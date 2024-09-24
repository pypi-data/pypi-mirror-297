from flask import current_app as app
from invenio_access.permissions import system_identity
from invenio_db import db
from invenio_files_rest.errors import InvalidKeyError
from invenio_rdm_records.proxies import (
    current_rdm_records_service as records_service,
)
from invenio_record_importer_kcworks.errors import (
    FileUploadError,
    UploadFileNotFoundError,
)
from invenio_record_importer_kcworks.utils.utils import (
    normalize_string,
    valid_date,
)
from invenio_records_resources.services.errors import (
    FileKeyNotFoundError,
)
from pprint import pformat
from pathlib import Path
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional
import unicodedata
from urllib.parse import unquote


class FilesHelper:
    def __init__(self):
        self.files_service = records_service.draft_files

    def handle_record_files(
        self,
        metadata: dict,
        file_data: dict,
        existing_record: Optional[dict] = None,
    ):
        print(f"handle_record_files metadata: {pformat(metadata)}")
        assert metadata["files"]["enabled"] is True
        uploaded_files = {}
        same_files = False

        if existing_record:
            same_files = self._compare_existing_files(
                metadata["id"],
                existing_record["is_draft"] is True
                and existing_record["is_published"] is False,
                existing_record["files"]["entries"],
                file_data["entries"],
            )

        if same_files:
            app.logger.info(
                "    skipping uploading files (same already uploaded)..."
            )
        else:
            app.logger.info("    uploading new files...")

            uploaded_files = self._upload_draft_files(
                metadata["id"],
                file_data["entries"],
                {
                    next(iter(file_data["entries"])): metadata[
                        "custom_fields"
                    ]["hclegacy:file_location"]
                },
            )
        return uploaded_files

    def _retry_file_initialization(self, draft_id: str, k: str) -> bool:
        existing_record = self.files_service._get_record(
            draft_id, system_identity, "create_files"
        )

        if existing_record.files.entries[k] == {"metadata": {}}:
            removed_file = existing_record.files.delete(
                k, softdelete_obj=False, remove_rf=True
            )
            db.session.commit()
            app.logger.debug(
                "...file key existed on record but was empty and was "
                "removed. This probably indicates a prior failed upload."
            )
            app.logger.debug(pformat(removed_file))

            initialization = self.files_service.init_files(
                system_identity, draft_id, data=[{"key": k}]
            ).to_dict()
            assert (
                len(
                    [
                        e["key"]
                        for e in initialization["entries"]
                        if e["key"] == k
                    ]
                )
                == 1
            )
            return True
        else:
            app.logger.error(existing_record.files.entries[k].to_dict())
            app.logger.error(
                "    file key already exists on record but is not found in "
                "draft metadata retrieved by record service"
            )
            raise InvalidKeyError(
                f"File key {k} already exists on record but is not found in "
                "draft metadata retrieved by record service"
            )

    def _upload_draft_files(
        self,
        draft_id: str,
        files_dict: dict[str, dict],
        source_filenames: dict[str, str],
    ) -> dict:
        output = {}

        for k, v in files_dict.items():
            source_filename = source_filenames[k]
            long_filename = source_filename.replace(
                "/srv/www/commons/current/web/app/uploads/humcore/", ""
            )
            long_filename = long_filename.replace(
                "/srv/www/commons/shared/uploads/humcore/", ""
            )
            app.logger.debug(k)
            app.logger.debug(source_filename)
            app.logger.debug(normalize_string(k))
            app.logger.debug(normalize_string(unquote(source_filename)))
            try:
                assert normalize_string(k) in normalize_string(
                    unquote(source_filename)
                )
            except AssertionError:
                app.logger.error(
                    f"    file key {k} does not match source filename"
                    f" {source_filename}..."
                )
                raise UploadFileNotFoundError(
                    f"File key from metadata {k} not found in source file path"
                    f" {source_filename}"
                )
            file_path = (
                Path(app.config["RECORD_IMPORTER_FILES_LOCATION"])
                / long_filename
            )
            app.logger.debug(f"    uploading file: {file_path}")
            try:
                assert file_path.is_file()
            except AssertionError:
                try:
                    full_length = len(long_filename.split("."))
                    try_index = -2
                    while abs(try_index) + 2 <= full_length:
                        file_path = Path(
                            app.config["RECORD_IMPORTER_FILES_LOCATION"],
                            ".".join(long_filename.split(".")[:try_index])
                            + "."
                            + k,
                        )
                        if file_path.is_file():
                            break
                        else:
                            try_index -= 1
                    assert file_path.is_file()
                except AssertionError:
                    try:
                        file_path = Path(
                            unicodedata.normalize("NFD", str(file_path))
                        )
                        assert file_path.is_file()
                    except AssertionError:
                        raise UploadFileNotFoundError(
                            f"    file not found for upload {file_path}..."
                        )

            try:
                initialization = self.files_service.init_files(
                    system_identity, draft_id, data=[{"key": k}]
                ).to_dict()
                assert (
                    len(
                        [
                            e["key"]
                            for e in initialization["entries"]
                            if e["key"] == k
                        ]
                    )
                    == 1
                )
            except InvalidKeyError:
                self._retry_file_initialization(draft_id, k)
            except Exception as e:
                app.logger.error(
                    f"    failed to initialize file upload for {draft_id}..."
                )
                raise e

            try:
                with open(
                    file_path,
                    "rb",
                ) as binary_file_data:
                    binary_file_data.seek(0)
                    self.files_service.set_file_content(
                        system_identity, draft_id, k, binary_file_data
                    )

            except Exception as e:
                app.logger.error(
                    f"    failed to upload file content for {draft_id}..."
                )
                raise e

            try:
                self.files_service.commit_file(system_identity, draft_id, k)
            except Exception as e:
                app.logger.error(
                    f"    failed to commit file upload for {draft_id}..."
                )
                raise e

            output[k] = "uploaded"

        result_record = self.files_service.list_files(
            system_identity, draft_id
        ).to_dict()
        try:
            assert all(
                r["key"]
                for r in result_record["entries"]
                if r["key"] in files_dict.keys()
            )
            for v in result_record["entries"]:
                assert v["key"] == k
                assert v["status"] == "completed"
                app.logger.debug(f"size: {v['size']}  {files_dict[k]['size']}")
                if str(v["size"]) != str(files_dict[k]["size"]):
                    raise FileUploadError(
                        f"Uploaded file size ({v['size']}) does not match "
                        f"expected size ({files_dict[k]['size']})"
                    )
                assert valid_date(v["created"])
                assert valid_date(v["updated"])
                assert not v["metadata"]
        except AssertionError:
            app.logger.error(
                "    failed to properly upload file content for"
                f" draft {draft_id}..."
            )
            app.logger.error(f"result is {pformat(result_record['entries'])}")

        return output

    def _compare_existing_files(
        self,
        draft_id: str,
        is_draft: bool,
        old_files: dict[str, dict],
        new_entries: dict[str, dict],
    ) -> bool:
        files_service = (
            records_service.files
            if not is_draft
            else records_service.draft_files
        )
        same_files = True

        try:
            files_request = files_service.list_files(
                system_identity, draft_id
            ).to_dict()
        except NoResultFound:
            try:
                files_request = records_service.draft_files.list_files(
                    system_identity, draft_id
                ).to_dict()
            except NoResultFound:
                files_request = None
        existing_files = (
            files_request.get("entries", []) if files_request else []
        )
        if len(existing_files) == 0:
            same_files = False
            app.logger.info("    no files attached to existing record")
        else:
            for k, v in new_entries.items():
                wrong_file = False
                existing_file = [
                    f
                    for f in existing_files
                    if unicodedata.normalize("NFC", f["key"])
                    == unicodedata.normalize("NFC", k)
                ]

                if len(existing_file) == 0:
                    same_files = False

                elif (existing_file[0]["status"] == "pending") or (
                    str(v["size"]) != str(existing_file[0]["size"])
                ):
                    same_files = False
                    wrong_file = True

                if wrong_file:
                    error_message = (
                        "Existing record with same DOI has different"
                        f" files.\n{pformat(old_files)}\n !=\n "
                        f"{pformat(new_entries)}\n"
                        f"Could not delete existing file "
                        f"{existing_file[0]['key']}."
                    )
                    try:
                        app.logger.info(
                            "    existing record had wrong or partial upload,"
                            " now deleted"
                        )
                    except NoResultFound:
                        records_service.draft_files.delete_file(
                            system_identity, draft_id, existing_file[0]["key"]
                        )
                    except FileKeyNotFoundError as e:
                        app.logger.info(
                            "    existing record had wrong or partial upload,"
                            " but it could not be found for deletion"
                        )
                        raise e
                    except Exception as e:
                        raise e

                    try:
                        files_service.list_files(
                            system_identity, draft_id
                        ).to_dict()["entries"]
                    except NoResultFound:
                        app.logger.info(
                            "    deleted file is no longer attached to record"
                        )
                    else:
                        app.logger.error(error_message)
                        raise RuntimeError(error_message)
            return same_files
