import json
import os
from typing import Callable, Generator, List, Optional

from openai import OpenAI

from ..types import BaseTool, Message, OnFcMethods
from ..utils import ChunkUtils, ConvertUtils
from .store import Files

_MAX_ITER = 3


class LLM:
    def __init__(
        self,
        client: OpenAI,
        model: Optional[str] = None,
        can_use_tools: Optional[bool] = False,
    ) -> None:
        self.set()
        self.client = client
        self.model = model
        self.can_use_tools = can_use_tools

    def set(
        self,
        on_chunk: Optional[Callable[[str], None]] = None,
        on_fc: Optional[OnFcMethods] = None,
        file_uri: Optional[str] = None,
    ):
        self.on_chunk = on_chunk if on_chunk else ChunkUtils.to_console
        self.on_fc = on_fc if on_fc else {}
        self.on_fc["meta"] = self.on_fc.get("meta", ChunkUtils.to_null)
        self.on_fc["params"] = self.on_fc.get("params", ChunkUtils.to_null)
        self.on_fc["result"] = self.on_fc.get("result", ChunkUtils.to_null)
        _FILE_URI = os.environ.get("GPTLITE_FILE_URI", None)

        self.file_uri = file_uri or _FILE_URI

    def chat(
        self,
        tools: Optional[List[BaseTool]] = None,
        iter: Optional[int] = 0,
        **params,
    ) -> Generator[Message, None, None]:
        iter = iter or 0
        if iter > _MAX_ITER + 1:
            raise Exception("Maximum number of iterations reached")

        if self.can_use_tools and tools is not None:
            openai_tools = [
                ConvertUtils.convert_to_openai_tool(tool) for tool in tools
            ]
            stream = self._call_llm(**params, tools=openai_tools)
        else:
            stream = self._call_llm(**params)

        new_messages = []
        content = ""
        for type, chunk in stream:
            if type == "content":
                content += chunk
            elif type == "tool_calls":
                tool_calls = chunk
                # NOTE: "content": "" is necessary for qwen models
                tool_call_message: Message = {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": tool_calls,
                }
                new_messages.append(tool_call_message)
                yield tool_call_message

                results = self._exec_tool_calls(
                    tool_calls=tool_calls, tools=tools
                )
                for result in results:
                    new_messages.append(result)
                    yield result

                if new_messages[-1].get("role") != "assistant":
                    new_params = params.copy()
                    new_params["messages"] = []
                    for message in params["messages"]:
                        new_params["messages"].append(message)
                    for message in new_messages:
                        new_params["messages"].append(message)
                    summary_messages = self.chat(
                        **new_params, iter=iter + 1, tools=tools
                    )
                    for message in summary_messages:
                        new_messages.append(message)
                        yield message
                else:
                    yield new_messages[-1]

        if content != "":
            assistant_message: Message = {
                "role": "assistant",
                "content": content,
            }
            new_messages.append(assistant_message)
            yield assistant_message

    def _exec_tool_calls(
        self, tool_calls, tools
    ) -> Generator[Message, None, None]:
        for tool_call in tool_calls:
            if tool_call["type"] == "function":
                function_name = tool_call["function"]["name"]
                function_args = tool_call["function"]["arguments"]
                tool = next(
                    filter(lambda tool: tool.name == function_name, tools),
                    None,
                )
                if tool is None:
                    content = (
                        f"工具[{function_name}]不存在，停止继续调用工具。"
                    )
                    yield self._on_tool_call_exception(content)
                    return
                try:
                    content = ""
                    params = json.loads(function_args)

                    result = tool.run(params)

                    if result["type"] == "string":
                        content = result["data"]
                    elif result["type"] == "json":
                        content = json.dumps(
                            result["data"], ensure_ascii=False
                        )
                    elif result["type"] == "bytes":
                        info = Files.create(
                            f"{tool.name}", result["data"], "tool_call"
                        )
                        assert self.file_uri is not None, "File URI is not set"
                        uri = self.file_uri.replace("{id}", info["id"])
                        obj = {
                            "file": info,
                            "uri": uri,
                            "message": f"已将计算结果存储在文件中，请告知用户可以通过 [{info['id']}]({uri}) 获取结果",
                        }
                        content = json.dumps(obj, ensure_ascii=False)

                    self.on_fc["result"](content)
                    message: Message = {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        # "name": function_name, # NOT EXIST in tool call message
                        "content": content,
                    }
                    yield message
                except Exception as e:
                    content = f"工具[{function_name}]调用出错，停止继续调用工具。以下是出错情况：\n{'='*10}\n{str(e)}\n{'='*10}"
                    yield self._on_tool_call_exception(content)

    def _on_tool_call_exception(self, content: str):
        self.on_fc["result"](content)
        exception_message: Message = {
            "role": "assistant",
            "content": content,
        }
        return exception_message

    def _call_llm(self, **params):
        def generator(completions):
            tool_calls = []
            if "stream" in params and params["stream"]:
                for chunk in completions:
                    choice = chunk.choices[0]
                    if choice.delta.tool_calls is not None:
                        self._append_stream_delta_tool_calls(
                            choice.delta.tool_calls, tool_calls
                        )
                        # NOTE: it is a fix for Yi-Large-FC model
                        #       other models will generate a chunk with tool_calls=None in the last message
                        if choice.finish_reason == "tool_calls":
                            yield "tool_calls", tool_calls
                            return
                    elif choice.finish_reason == "tool_calls":
                        yield "tool_calls", tool_calls
                    else:
                        if choice.delta.content is not None:
                            self.on_chunk(choice.delta.content)
                            yield "content", choice.delta.content
            else:
                choice = completions.choices[0]
                if choice.finish_reason == "tool_calls":
                    tool_calls = choice.message.tool_calls
                    converted = []
                    for tool_call in tool_calls:
                        meta = {
                            "id": tool_call.id,
                            "type": tool_call.type,
                            "name": tool_call.function.name,
                        }
                        self.on_fc["meta"](meta)
                        self.on_fc["params"](tool_call.function.arguments)
                        item = {
                            "function": {
                                "arguments": tool_call.function.arguments
                            }
                        }
                        self._tool_call_to_dict(tool_call, item)
                        converted.append(item)
                    yield "tool_calls", converted
                else:
                    self.on_chunk(choice.message.content)
                    yield "content", choice.message.content

        if "model" not in params:
            params["model"] = self.model
        completions = self.client.chat.completions.create(**params)
        return generator(completions)

    def _append_stream_delta_tool_calls(self, delta_tool_calls, tool_calls):
        for i, delta_tool_call in enumerate(delta_tool_calls):
            if len(tool_calls) <= i:
                tool_calls.append({"function": {"arguments": ""}})

            if delta_tool_call.function.name is not None:
                self._tool_call_to_dict(delta_tool_call, tool_calls[i])
                fc_meta = {
                    "id": tool_calls[i]["id"],
                    "type": tool_calls[i]["type"],
                    "name": tool_calls[i]["function"]["name"],
                }
                self.on_fc["meta"](fc_meta)
            tool_calls[i]["function"][
                "arguments"
            ] += delta_tool_call.function.arguments
            self.on_fc["params"](delta_tool_call.function.arguments)

    def _tool_call_to_dict(self, tool_call, d):
        d["function"]["name"] = tool_call.function.name
        d["id"] = tool_call.id
        d["type"] = tool_call.type
