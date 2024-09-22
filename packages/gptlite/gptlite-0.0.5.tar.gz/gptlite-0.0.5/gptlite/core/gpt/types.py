from typing import List, Optional

from yaml import safe_load

from gptlite.core.llm import LLM
from gptlite.types import BaseTool, Message


class GPT:
    name: str
    desc: Optional[str] = None
    prompt: str
    single: Optional[bool] = False
    tools: Optional[List[BaseTool]] = []

    llm: Optional[LLM] = None

    def __init__(
        self,
        name: str,
        desc: Optional[str] = None,
        prompt: Optional[str] = None,
        single: Optional[bool] = None,
        tools: Optional[List[BaseTool]] = None,
    ):
        self.name = name
        self.desc = desc or ""
        self.prompt = prompt or "You are a helpful assistant."
        self.single = single or False
        self.tools = tools or None

    def set_llm(self, llm: LLM):
        self.llm = llm

    @staticmethod
    def from_yaml(yaml_file: str, tool_repo: Optional[List[BaseTool]] = []):
        gpt = safe_load(open(yaml_file, "r"))

        assert gpt is not None, f"{yaml_file} : not a valid yaml file"
        assert "name" in gpt, f"{yaml_file} : [gpt should have a valid name]"

        names = gpt.get("tools", [])
        tools = [tool for tool in (tool_repo or []) if tool.name in names]
        gpt["tools"] = tools

        return GPT(**gpt)

    def chat(self, messages: List[Message], **params):
        assert self.llm, "Should call gpt.set_llm(llm, model) first."
        assert (
            messages is not None and len(messages) > 0
        ), "gptlite.GPT.chat() : messages should be None or empty"

        if messages[0]["role"] != "system":
            messages.insert(0, {"role": "system", "content": self.prompt})

        if self.single:
            system = messages[0]
            last = messages[-1] if len(messages) > 1 else None
            messages = [system, last] if last else []

        yield from self.llm.chat(tools=self.tools, messages=messages, **params)
