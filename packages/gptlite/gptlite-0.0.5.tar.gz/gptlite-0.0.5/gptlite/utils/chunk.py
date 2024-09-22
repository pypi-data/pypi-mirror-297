from typing import Union


class ChunkUtils:
    @staticmethod
    def to_console(chunk: Union[str, dict]) -> None:
        if isinstance(chunk, dict):
            print(chunk)
        else:
            print(chunk, end="", flush=True)

    @staticmethod
    def to_file(chunk: Union[str, dict]) -> None:
        pass

    @staticmethod
    def to_null(chunk: Union[str, dict]) -> None:
        pass
