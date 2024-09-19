# @Author: Bi Ying
# @Date:   2024-07-26 14:48:55
import re
import json
from math import ceil
import httpx
import tiktoken
from anthropic import Anthropic
from qwen_tokenizer import qwen_tokenizer
from deepseek_tokenizer import deepseek_tokenizer

from ..settings import settings
from ..utilities.retry import Retry
from ..types.enums import BackendType
from ..utilities.media_processing import ImageProcessor


chatgpt_encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
gpt_4o_encoding = tiktoken.encoding_for_model("gpt-4o")


class ToolCallContentProcessor:
    tool_use_re = re.compile(r"<\|▶\|>(.*?)<\|◀\|>", re.DOTALL)

    def __init__(self, content: str):
        self.content = content

    @property
    def non_tool_content(self):
        return re.sub(self.tool_use_re, "", self.content).strip()

    @property
    def tool_calls(self):
        if "<|▶|>" not in self.content or "<|◀|>" not in self.content:
            return {}
        tool_calls_matches = re.findall(self.tool_use_re, self.content)
        if tool_calls_matches:
            tool_call_data = {}
            for match in tool_calls_matches:
                try:
                    tool_call_data = json.loads(match)
                except json.JSONDecodeError:
                    print(f"Failed to parse tool call data:\nContent: {self.content}\nMatch: {match}")

            if not tool_call_data:
                return {}

            arguments = json.dumps(tool_call_data["arguments"], ensure_ascii=False)
            return {
                "tool_calls": [
                    {
                        "index": 0,
                        "id": "call_0",
                        "function": {
                            "arguments": arguments,
                            "name": tool_call_data["name"],
                        },
                        "type": "function",
                    }
                ]
            }
        else:
            return {}


def get_assistant_role_key(backend: BackendType) -> str:
    if backend == BackendType.Gemini:
        return "model"
    else:
        return "assistant"


def get_content_key(backend: BackendType) -> str:
    if backend == BackendType.Gemini:
        return "parts"
    else:
        return "content"


def convert_type(value, value_type):
    if value_type == "string":
        return str(value)
    elif value_type == "number":
        try:
            return float(value)
        except ValueError:
            return value
    elif value_type == "integer":
        try:
            return int(value)
        except ValueError:
            return value
    elif value_type == "boolean":
        return value.lower() in ("true", "1", "t")
    else:
        return value  # 如果类型未知，返回原始值


def get_token_counts(text: str | dict, model: str = "") -> int:
    if not isinstance(text, str):
        text = str(text)
    if model == "gpt-3.5-turbo":
        return len(chatgpt_encoding.encode(text))
    elif model in ("gpt-4o", "gpt-4o-mini"):
        return len(gpt_4o_encoding.encode(text))
    elif model.startswith("abab"):
        model_setting = settings.minimax.models[model]
        if len(model_setting.endpoints) == 0:
            return int(len(text) / 1.33)
        endpoint_id = model_setting.endpoints[0]
        endpoint = settings.get_endpoint(endpoint_id)
        tokenize_url = "https://api.minimax.chat/v1/tokenize"
        headers = {"Authorization": f"Bearer {endpoint.api_key}", "Content-Type": "application/json"}
        request_body = {
            "model": model,
            "tokens_to_generate": 128,
            "temperature": 0.2,
            "messages": [
                {"sender_type": "USER", "text": text},
            ],
        }

        _, response = (
            Retry(httpx.post)
            .args(url=tokenize_url, headers=headers, json=request_body, timeout=None)
            .retry_times(5)
            .sleep_time(10)
            .run()
        )
        response = response.json()
        return response["segments_num"]
    elif model in ("moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"):
        model_setting = settings.moonshot.models[model]
        if len(model_setting.endpoints) == 0:
            return len(chatgpt_encoding.encode(text))
        endpoint_id = model_setting.endpoints[0]
        endpoint = settings.get_endpoint(endpoint_id)
        tokenize_url = "https://api.moonshot.cn/v1/tokenizers/estimate-token-count"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {endpoint.api_key}"}
        request_body = {
            "model": model,
            "messages": [
                {"role": "user", "content": text},
            ],
        }
        _, response = (
            Retry(httpx.post)
            .args(url=tokenize_url, headers=headers, json=request_body, timeout=None)
            .retry_times(5)
            .sleep_time(10)
            .run()
        )
        response = response.json()
        return response["data"]["total_tokens"]
    elif model.startswith("gemini"):
        model_setting = settings.gemini.models[model]
        if len(model_setting.endpoints) == 0:
            return len(chatgpt_encoding.encode(text))
        endpoint_id = model_setting.endpoints[0]
        endpoint = settings.get_endpoint(endpoint_id)
        url = f"{endpoint.api_base}/models/{model_setting.id}:countTokens"
        params = {"key": endpoint.api_key}
        request_body = {
            "contents": {
                "role": "USER",
                "parts": [
                    {"text": "TEXT"},
                ],
            },
        }
        _, response = (
            Retry(httpx.post)
            .args(url, json=request_body, params=params, timeout=None)
            .retry_times(5)
            .sleep_time(10)
            .run()
        )
        result = response.json()
        return result["totalTokens"]
    elif model.startswith("claude"):
        return Anthropic().count_tokens(text)
    elif model.startswith("deepseek"):
        return len(deepseek_tokenizer.encode(text))
    elif model.startswith("qwen"):
        return len(qwen_tokenizer.encode(text))
    else:
        return len(chatgpt_encoding.encode(text))


def calculate_image_tokens(width: int, height: int, model: str = "gpt-4o"):
    if width > 2048 or height > 2048:
        aspect_ratio = width / height
        if aspect_ratio > 1:
            width, height = 2048, int(2048 / aspect_ratio)
        else:
            width, height = int(2048 * aspect_ratio), 2048

    if width >= height and height > 768:
        width, height = int((768 / height) * width), 768
    elif height > width and width > 768:
        width, height = 768, int((768 / width) * height)

    tiles_width = ceil(width / 512)
    tiles_height = ceil(height / 512)
    total_tokens = 85 + 170 * (tiles_width * tiles_height)

    return total_tokens


def get_message_token_counts(messages: list, tools: dict | None = None, model: str = "gpt-4o") -> int:
    tokens = 0
    formatted_messages = format_messages(messages, backend=BackendType.OpenAI, native_multimodal=True)
    for message in formatted_messages:
        content = message["content"]
        if isinstance(content, str):
            tokens += get_token_counts(content, model)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item["type"] == "text":
                    tokens += get_token_counts(item["text"], model)
                elif isinstance(item, dict) and item["type"].startswith("image"):
                    # TODO: Get real image size
                    tokens += calculate_image_tokens(2048, 2048, model)
    if tools is not None:
        tokens += get_token_counts(str(tools), model)

    return tokens


def cutoff_messages(
    messages: list,
    max_count: int = 16000,
    backend: BackendType = BackendType.OpenAI,
    model: str = "",
) -> list:
    """
    给定一个消息列表和最大长度，将消息列表截断到最大长度。
    如果列表中第一个元素的role是'system'，则始终保留该元素。
    超过长度时从列表开始处（第二个元素起）依次删除消息，直到总长度小于等于最大长度。
    如果最后一条消息超过了最大长度，那么将最后一条消息截断到最大长度。

    Args:
        messages (list): 消息列表，每条消息是一个包含'role'和'content'的字典。
        max_count (int, optional): 允许的最大长度。默认值为16000。

    Returns:
        list: 截断后的消息列表。
    """

    if len(messages) == 0:
        return messages

    messages_length = 0
    content_key = get_content_key(backend)

    # 先检查并保留第一条system消息（如果有）
    system_message = None
    if messages[0]["role"] == "system":
        system_message = messages[0]
        system_message_length = get_token_counts(system_message[content_key], model)
        if system_message_length > max_count:
            # 如果第一条system消息超过最大长度，截断它
            system_message[content_key] = system_message[content_key][-max_count:]
            return [system_message]
        else:
            messages_length += system_message_length
            messages = messages[1:]  # 移除第一个元素，以处理其余消息

    if system_message:
        system_message = [system_message]
    else:
        system_message = []

    for index, message in enumerate(reversed(messages)):
        if not message[content_key]:
            continue
        count = 0
        if isinstance(message[content_key], str):
            contents = [message[content_key]]
        elif isinstance(message[content_key], list):
            contents = message[content_key]
        else:
            contents = [str(message[content_key])]

        for content in contents:
            # TODO: Add non text token counts
            if isinstance(content, dict) and "text" not in content:
                continue
            if isinstance(content, dict):
                content_text = content["text"]
            else:
                content_text = str(content)
            count += get_token_counts(content_text, model)
        messages_length += count
        if messages_length < max_count:
            continue
        if index == 0:
            # 一条消息就超过长度则将该消息内容进行截断，保留该消息最后的一部分
            if backend == BackendType.Gemini:
                message[content_key] = [{"text": message[content_key][-max_count:]}]
            else:
                content = message[content_key][max_count - messages_length :]
            return system_message + [
                {
                    "role": message["role"],
                    content_key: content,
                }
            ]
        return system_message + messages[-index:]
    return system_message + messages


def format_image_message(image: str, backend: BackendType = BackendType.OpenAI) -> dict:
    image_processor = ImageProcessor(image_source=image)
    if backend == BackendType.OpenAI:
        return {
            "type": "image_url",
            "image_url": {"url": image_processor.data_url},
        }
    elif backend == BackendType.Anthropic:
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": image_processor.mime_type,
                "data": image_processor.base64_image,
            },
        }
    elif backend == BackendType.Gemini:
        return {
            "inline_data": {
                "mime_type": image_processor.mime_type,
                "data": image_processor.base64_image,
            }
        }
    else:
        return {
            "type": "image_url",
            "image_url": {"url": image_processor.data_url},
        }


def format_workflow_messages(message, content, backend):
    formatted_messages = []

    # 工具调用消息
    if backend in (BackendType.OpenAI, BackendType.ZhiPuAI, BackendType.Mistral, BackendType.Yi):
        tool_call_message = {
            "content": None,
            "role": "assistant",
            "tool_calls": [
                {
                    "id": message["metadata"]["selected_workflow"]["tool_call_id"],
                    "type": "function",
                    "function": {
                        "name": message["metadata"]["selected_workflow"]["function_name"],
                        "arguments": json.dumps(message["metadata"]["selected_workflow"]["params"]),
                    },
                }
            ],
        }
    elif backend == BackendType.Anthropic:
        tool_call_message = {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "id": message["metadata"]["selected_workflow"]["tool_call_id"],
                    "name": message["metadata"]["selected_workflow"]["function_name"],
                    "input": message["metadata"]["selected_workflow"]["params"],
                },
            ],
        }
        if content:
            tool_call_message["content"].insert(0, {"type": "text", "text": content})
    elif backend == BackendType.Gemini:
        tool_call_message = {
            "role": "model",
            "parts": [
                {
                    "functionCall": {
                        "name": message["metadata"]["selected_workflow"]["function_name"],
                        "args": message["metadata"]["selected_workflow"]["params"],
                    }
                },
            ],
        }
        if content:
            tool_call_message["parts"].insert(0, {"text": content})
    else:
        tool_call_message = {
            "content": json.dumps(
                {
                    "name": message["metadata"]["selected_workflow"]["function_name"],
                    "arguments": json.dumps(message["metadata"]["selected_workflow"]["params"]),
                },
                ensure_ascii=False,
            ),
            "role": "assistant",
        }
    formatted_messages.append(tool_call_message)

    # 工具调用结果消息
    if backend in (BackendType.OpenAI, BackendType.ZhiPuAI, BackendType.Mistral, BackendType.Yi):
        tool_call_result_message = {
            "role": "tool",
            "tool_call_id": message["metadata"]["selected_workflow"]["tool_call_id"],
            "name": message["metadata"]["selected_workflow"]["function_name"],
            "content": message["metadata"].get("workflow_result", ""),
        }
    elif backend == BackendType.Anthropic:
        tool_call_result_message = {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": message["metadata"]["selected_workflow"]["tool_call_id"],
                    "content": message["metadata"].get("workflow_result", ""),
                }
            ],
        }
    elif backend == BackendType.Gemini:
        tool_call_result_message = {
            "role": "function",
            "parts": [
                {
                    "functionResponse": {
                        "name": message["metadata"]["selected_workflow"]["function_name"],
                        "response": {
                            "name": message["metadata"]["selected_workflow"]["function_name"],
                            "content": message["metadata"].get("workflow_result", ""),
                        },
                    }
                }
            ],
        }
    else:
        tool_call_result_message = {
            "role": "user",
            "content": json.dumps(
                {
                    "function": message["metadata"]["selected_workflow"]["function_name"],
                    "result": message["metadata"].get("workflow_result", ""),
                },
                ensure_ascii=False,
            ),
        }
    formatted_messages.append(tool_call_result_message)

    if content and backend not in (BackendType.Mistral, BackendType.Anthropic, BackendType.Gemini):
        formatted_messages.append({"role": "assistant", "content": content})

    return formatted_messages


def format_openai_message(message, backend):
    role = message.get("role", "user")
    content = message.get("content", "")

    if backend == BackendType.Gemini:
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, str):
                    parts.append({"text": item})
                elif isinstance(item, dict) and "type" in item:
                    if item["type"] == "image":
                        parts.append({"image": item["image"]})
                    elif item["type"] == "text":
                        parts.append({"text": item["text"]})
            return {"role": "user" if role == "user" else "model", "parts": parts}
        else:
            return {"role": "user" if role == "user" else "model", "parts": [{"text": content}]}
    elif backend == BackendType.Anthropic:
        if isinstance(content, list):
            formatted_content = []
            for item in content:
                if isinstance(item, str):
                    formatted_content.append({"type": "text", "text": item})
                elif isinstance(item, dict) and "type" in item:
                    formatted_content.append(item)
            return {"role": role, "content": formatted_content}
        else:
            return {"role": role, "content": content}
    else:
        return message  # 对于其他后端，保持原样


def format_messages(
    messages: list,
    backend: BackendType = BackendType.OpenAI,
    native_multimodal: bool = False,
) -> list:
    """将 VectorVein 和 OpenAI 的 Message 序列化后的格式转换为不同模型支持的格式

    Args:
        messages (list): VectorVein Or OpenAI messages list.
        backend (str, optional): Messages format target backend. Defaults to BackendType.OpenAI.
        native_multimodal (bool, optional): Use native multimodal ability. Defaults to False.

    Returns:
        list: 转换后的消息列表
    """

    def is_vectorvein_message(message):
        return "content_type" in message

    backend = backend.lower()
    formatted_messages = []

    for message in messages:
        if is_vectorvein_message(message):
            # 处理 VectorVein 格式的消息
            content = message["content"]["text"]
            if message["content_type"] == "TXT":
                role = "user" if message["author_type"] == "U" else get_assistant_role_key(backend)
                formatted_message = format_text_message(
                    content, role, message.get("attachments", []), backend, native_multimodal
                )
                formatted_messages.append(formatted_message)
            elif message["content_type"] == "WKF" and message["status"] in ("S", "R"):
                formatted_messages.extend(format_workflow_messages(message, content, backend))
        else:
            # 处理 OpenAI 格式的消息
            formatted_message = format_openai_message(message, backend)
            formatted_messages.append(formatted_message)

    return formatted_messages


def format_text_message(content, role, attachments, backend, native_multimodal):
    images_extensions = ("jpg", "jpeg", "png", "bmp")
    has_images = any(attachment.lower().endswith(images_extensions) for attachment in attachments)

    if attachments:
        content += "\n# Attachments:\n"
        content += "\n".join([f"- {attachment}" for attachment in attachments])

    if native_multimodal and has_images:
        if backend == BackendType.Gemini:
            parts = [{"text": content}]
            for attachment in attachments:
                if attachment.lower().endswith(images_extensions):
                    parts.append(format_image_message(image=attachment, backend=backend))
            return {"role": role, "parts": parts}
        else:
            return {
                "role": role,
                "content": [
                    {"type": "text", "text": content},
                    *[
                        format_image_message(image=attachment, backend=backend)
                        for attachment in attachments
                        if attachment.lower().endswith(images_extensions)
                    ],
                ],
            }
    else:
        if backend == BackendType.Gemini:
            return {"role": role, "parts": [{"text": content}]}
        elif backend == BackendType.Anthropic:
            return {"role": role, "content": content}
        else:
            return {"role": role, "content": content}


def generate_tool_use_system_prompt(tools: list, format_type: str = "json") -> str:
    if format_type == "json":
        return (
            "You have access to the following tools. Use them if required and wait for the tool call result. Stop output after calling a tool.\n\n"
            f"# Tools\n{tools}\n\n"
            "# Requirements when using tools\n"
            "Must starts with <|▶|> and ends with <|◀|>\n"
            "Must be valid JSON format and pay attention to escape characters.\n"
            '## Output format\n<|▶|>{"name": "<function name:str>", "arguments": <arguments:dict>}<|◀|>\n\n'
            '## Example output\n<|▶|>{"name": "get_current_weather", "arguments": {"location": "San Francisco, CA"}}<|◀|>'
        )
    elif format_type == "xml":
        return (
            "You have access to the following tools. Use them if required and wait for the tool call result. Stop output after calling a tool.\n\n"
            f"# Tools\n{tools}\n\n"
            "# Requirements when using tools\n"
            "Must starts with <|▶|> and ends with <|◀|>\n"
            "Must be valid XML format.\n"
            "## Output format\n<|▶|><invoke><tool_name>[function name:str]</tool_name><parameters><parameter_1_name>[parameter_1_value]</parameter_1_name><parameter_2_name>[parameter_2_value]</parameter_2_name>...</parameters></invoke><|◀|>\n\n"
            "## Example output\n<|▶|><invoke><tool_name>calculator</tool_name><parameters><first_operand>1984135</first_operand><second_operand>9343116</second_operand><operator>*</operator></parameters></invoke><|◀|>"
        )
