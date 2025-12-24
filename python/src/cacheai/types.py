"""Cache AI Python API type definitions."""

from typing import List, Optional, Union, Literal
from pydantic import BaseModel, Field


# ========================================
# Chat Completion Types
# ========================================

class ChatMessage(BaseModel):
    """A message in a chat completion."""

    role: Literal["system", "user", "assistant", "tool"]
    content: Optional[str] = None
    name: Optional[str] = None
    tool_calls: Optional[List[dict]] = None
    tool_call_id: Optional[str] = None


class ChatCompletionChoice(BaseModel):
    """A choice in a chat completion response."""

    index: int
    message: ChatMessage
    finish_reason: Optional[str] = None


class Usage(BaseModel):
    """Token usage information."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletion(BaseModel):
    """Chat completion response."""

    id: str
    object: Literal["chat.completion"] = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Optional[Usage] = None
    system_fingerprint: Optional[str] = None


# ========================================
# Streaming Types
# ========================================

class ChatCompletionChunkDelta(BaseModel):
    """Delta in a streaming chunk."""

    role: Optional[str] = None
    content: Optional[str] = None


class ChatCompletionChunkChoice(BaseModel):
    """A choice in a streaming chunk."""

    index: int
    delta: ChatCompletionChunkDelta
    finish_reason: Optional[str] = None


class ChatCompletionChunk(BaseModel):
    """A chunk in a streaming chat completion."""

    id: str
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    created: int
    model: str
    choices: List[ChatCompletionChunkChoice]
    system_fingerprint: Optional[str] = None


# ========================================
# Completion Types (Legacy)
# ========================================

class CompletionChoice(BaseModel):
    """A choice in a completion response."""

    text: str
    index: int
    logprobs: Optional[dict] = None
    finish_reason: Optional[str] = None


class Completion(BaseModel):
    """Completion response."""

    id: str
    object: Literal["text_completion"] = "text_completion"
    created: int
    model: str
    choices: List[CompletionChoice]
    usage: Optional[Usage] = None


# ========================================
# Models Types
# ========================================

class Model(BaseModel):
    """Model information."""

    id: str
    object: Literal["model"] = "model"
    created: int
    owned_by: str


class ModelList(BaseModel):
    """List of models."""

    object: Literal["list"] = "list"
    data: List[Model]
