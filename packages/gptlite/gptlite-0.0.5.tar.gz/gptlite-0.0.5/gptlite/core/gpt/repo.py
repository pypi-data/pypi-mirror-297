import os
from typing import Dict, List, Optional

from gptlite.core.llm import LLM
from gptlite.types import BaseTool

from .types import GPT


class GPTRepo:
    gpts: Dict[str, GPT] = {}

    def load_yamls(
        self, dirname: str, llm: LLM, tools: Optional[List[BaseTool]] = []
    ):
        yamls = [
            os.path.splitext(_file)[0]
            for _file in os.listdir(dirname)
            if _file.endswith(".yaml")
        ]
        for yaml_file in yamls:
            gpt = GPT.from_yaml(
                os.path.join(dirname, f"{yaml_file}.yaml"), tool_repo=tools
            )
            gpt.set_llm(llm=llm)
            self.put(gpt)

    def put(self, gpt: GPT):
        self.gpts[gpt.name] = gpt

    def get(self, name: str):
        return self.gpts.get(name, None)
