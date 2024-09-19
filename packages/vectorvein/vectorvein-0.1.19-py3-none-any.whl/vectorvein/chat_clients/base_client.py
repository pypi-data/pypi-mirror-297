# @Author: Bi Ying
# @Date:   2024-07-26 14:48:55
from abc import ABC, abstractmethod
from typing import Generator, AsyncGenerator, Any

import httpx
from openai._types import NotGiven, NOT_GIVEN
from openai import OpenAI, AsyncOpenAI, AzureOpenAI, AsyncAzureOpenAI
from anthropic import Anthropic, AnthropicVertex, AsyncAnthropic, AsyncAnthropicVertex

from ..settings import settings
from ..types import defaults as defs
from ..types.enums import ContextLengthControlType, BackendType
from ..types.llm_parameters import ChatCompletionMessage, ChatCompletionDeltaMessage


class BaseChatClient(ABC):
    DEFAULT_MODEL: str | None = None
    BACKEND_NAME: BackendType | None = None

    def __init__(
        self,
        model: str = "",
        stream: bool = False,
        temperature: float = 0.7,
        context_length_control: ContextLengthControlType = defs.CONTEXT_LENGTH_CONTROL,
        random_endpoint: bool = True,
        endpoint_id: str = "",
        http_client: httpx.Client | None = None,
        **kwargs,
    ):
        self.model = model or self.DEFAULT_MODEL
        self.stream = stream
        self.temperature = temperature
        self.context_length_control = context_length_control
        self.random_endpoint = random_endpoint
        self.endpoint_id = endpoint_id
        self.http_client = http_client

        self.backend_settings = settings.get_backend(self.BACKEND_NAME)

        if endpoint_id:
            self.endpoint_id = endpoint_id
            self.random_endpoint = False
            self.endpoint = settings.get_endpoint(self.endpoint_id)

    @property
    @abstractmethod
    def raw_client(self) -> OpenAI | AzureOpenAI | Anthropic | AnthropicVertex:
        pass

    @abstractmethod
    def create_completion(
        self,
        messages: list,
        model: str | None = None,
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list | NotGiven = NOT_GIVEN,
        tool_choice: str | NotGiven = NOT_GIVEN,
        **kwargs,
    ) -> ChatCompletionMessage | Generator[ChatCompletionDeltaMessage, Any, None]:
        pass

    def create_stream(
        self,
        messages: list,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list | NotGiven = NOT_GIVEN,
        tool_choice: str | NotGiven = NOT_GIVEN,
        **kwargs,
    ) -> Generator[ChatCompletionDeltaMessage, Any, None]:
        return self.create_completion(
            messages=messages,
            model=model,
            stream=True,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            tool_choice=tool_choice,
            **kwargs,
        )


class BaseAsyncChatClient(ABC):
    DEFAULT_MODEL: str | None = None
    BACKEND_NAME: BackendType | None = None

    def __init__(
        self,
        model: str = "",
        stream: bool = False,
        temperature: float = 0.7,
        context_length_control: ContextLengthControlType = defs.CONTEXT_LENGTH_CONTROL,
        random_endpoint: bool = True,
        endpoint_id: str = "",
        http_client: httpx.AsyncClient | None = None,
        **kwargs,
    ):
        self.model = model or self.DEFAULT_MODEL
        self.stream = stream
        self.temperature = temperature
        self.context_length_control = context_length_control
        self.random_endpoint = random_endpoint
        self.endpoint_id = endpoint_id
        self.http_client = http_client

        self.backend_settings = settings.get_backend(self.BACKEND_NAME)

        if endpoint_id:
            self.endpoint_id = endpoint_id
            self.random_endpoint = False
            self.endpoint = settings.get_endpoint(self.endpoint_id)

    @property
    @abstractmethod
    def raw_client(self) -> AsyncOpenAI | AsyncAzureOpenAI | AsyncAnthropic | AsyncAnthropicVertex:
        pass

    @abstractmethod
    async def create_completion(
        self,
        messages: list,
        model: str | None = None,
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list | NotGiven = NOT_GIVEN,
        tool_choice: str | NotGiven = NOT_GIVEN,
        **kwargs,
    ) -> ChatCompletionMessage | AsyncGenerator[ChatCompletionDeltaMessage, None]:
        pass

    async def create_stream(
        self,
        messages: list,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list | NotGiven = NOT_GIVEN,
        tool_choice: str | NotGiven = NOT_GIVEN,
        **kwargs,
    ) -> AsyncGenerator[ChatCompletionDeltaMessage, None]:
        return await self.create_completion(
            messages=messages,
            model=model,
            stream=True,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            tool_choice=tool_choice,
            **kwargs,
        )
