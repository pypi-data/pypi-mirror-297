from langchain_core.utils.function_calling import (
    convert_to_openai_tool as langchain_convert_to_openai_tool,
)


class ConvertUtils:
    @staticmethod
    def convert_to_openai_tool(tool):
        return langchain_convert_to_openai_tool(tool)
