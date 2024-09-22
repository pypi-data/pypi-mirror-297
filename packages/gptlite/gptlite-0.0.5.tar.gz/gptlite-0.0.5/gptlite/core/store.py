import os
from typing import Any, Literal, Optional
from uuid import uuid4

from ..types import FileInfo


class Files:
    _STORE_PATH: Any = None

    @staticmethod
    def set(key: Literal["store_path"], value: str):
        if key == "store_path":
            Files._STORE_PATH = value
            if not os.path.exists(Files._STORE_PATH):
                os.makedirs(Files._STORE_PATH)
        else:
            raise ValueError(f"Invalid gptlite Files key: {key}")

    @staticmethod
    def list():
        Files._check_store_path()
        files = []
        for raw_file_name in os.listdir(Files._STORE_PATH):
            file_info = Files._get_file_info(raw_file_name)
            if not file_info:
                continue
            files.append(file_info)
        return files

    @staticmethod
    def create(filename, content: bytes, purpose: str):
        Files._check_store_path()
        id = "file-" + str(uuid4()).replace("-", "")
        purpose = purpose.replace("_", "-")
        raw_file_name = f"{id}_{purpose}_{filename}"

        path = os.path.join(Files._STORE_PATH, raw_file_name)

        with open(path, "wb") as f:
            f.write(content)

        size = os.path.getsize(path)
        created_at = os.path.getctime(path)

        return Files._compose_file_info(
            id, filename, purpose, size, created_at
        )

    @staticmethod
    def read(id: str) -> Optional[bytes]:
        Files._check_store_path()
        file = Files._find_file(id)
        if file:
            path = os.path.join(Files._STORE_PATH, file)
            with open(path, "rb") as f:
                content = f.read()
                return content
        else:
            return None

    @staticmethod
    def delete(id: str):
        Files._check_store_path()
        deleted = False
        filename = Files._find_file(id)
        path = os.path.join(Files._STORE_PATH, filename)
        if path:
            os.remove(path)
            deleted = True

        return {"id": id, "deleted": deleted}

    @staticmethod
    def info(id: str):
        Files._check_store_path()
        raw_file_name = Files._find_file(id)
        if raw_file_name:
            return Files._get_file_info(raw_file_name)
        else:
            return None

    @staticmethod
    def _find_file(id: str):
        files = os.listdir(Files._STORE_PATH)
        for raw_file_name in files:
            if raw_file_name.startswith(id):
                return raw_file_name
        return None

    @staticmethod
    def _get_file_info(raw_file_name: str):
        fields = raw_file_name.split("_")
        if len(fields) != 3:
            return None

        id = fields[0]
        purpose = fields[1]
        filename = "_".join(fields[2:])
        path = os.path.join(Files._STORE_PATH, raw_file_name)
        size = os.path.getsize(path)
        created_at = os.path.getctime(path)

        return Files._compose_file_info(
            id, filename, purpose, size, created_at
        )

    @staticmethod
    def _compose_file_info(id, filename, purpose, size, created_at):
        return FileInfo(
            id=id,
            bytes=size,
            filename=filename,
            purpose=purpose,
            created_at=created_at,
        )

    @staticmethod
    def _check_store_path():
        if Files._STORE_PATH is None:
            _STORE_PATH = os.environ.get("GPTLITE_FILE_STORE_PATH", None)
            if _STORE_PATH is None:
                raise ValueError(
                    "Please set `store_path` by `GPTLITE_FILE_STORE_PATH` in .env"
                )
            else:
                if not os.path.exists(_STORE_PATH):
                    os.makedirs(_STORE_PATH)
                Files._STORE_PATH = _STORE_PATH
