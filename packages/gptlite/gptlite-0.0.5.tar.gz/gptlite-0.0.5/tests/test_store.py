import tempfile

from gptlite import Files


def test_store_list():
    with tempfile.TemporaryDirectory() as temp_dir:
        Files.set(key="store_path", value=temp_dir)
        assert Files.list() == []


def test_store_create():
    with tempfile.TemporaryDirectory() as temp_dir:
        Files.set(key="store_path", value=temp_dir)

        file = Files.create("test.txt", bytes("Hello World!", "utf-8"), "test")
        assert file["id"] is not None
        assert file["filename"].find("test.txt") != -1
        assert file["purpose"] == "test"
        assert file["bytes"] == 12
        assert file["created_at"] > 0

        assert Files.list() == [file]


def test_store_read():
    with tempfile.TemporaryDirectory() as temp_dir:
        Files.set(key="store_path", value=temp_dir)

        content = bytes("Hello World!", "utf-8")
        file = Files.create("test.txt", content, "test")
        assert Files.read(file["id"]) == content


def test_store_delete():
    with tempfile.TemporaryDirectory() as temp_dir:
        Files.set(key="store_path", value=temp_dir)
        assert Files.list() == []
        file = Files.create("test.txt", bytes("Hello World!", "utf-8"), "test")
        assert len(Files.list()) == 1

        Files.delete(file["id"])
        assert Files.list() == []


def test_store_info():
    with tempfile.TemporaryDirectory() as temp_dir:
        Files.set(key="store_path", value=temp_dir)
        assert Files.list() == []
        file = Files.create("test.txt", bytes("Hello World!", "utf-8"), "test")
        assert Files.info(file["id"]) == file

        assert Files.info("non-exist-file-id") == None
