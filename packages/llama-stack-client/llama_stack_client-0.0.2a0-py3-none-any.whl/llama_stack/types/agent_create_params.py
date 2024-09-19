# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .shield_definition_param import ShieldDefinitionParam
from .tool_param_definition_param import ToolParamDefinitionParam
from .shared_params.sampling_params import SamplingParams
from .rest_api_execution_config_param import RestAPIExecutionConfigParam
from .llm_query_generator_config_param import LlmQueryGeneratorConfigParam
from .custom_query_generator_config_param import CustomQueryGeneratorConfigParam
from .default_query_generator_config_param import DefaultQueryGeneratorConfigParam

__all__ = [
    "AgentCreateParams",
    "AgentConfig",
    "AgentConfigTool",
    "AgentConfigToolSearchToolDefinition",
    "AgentConfigToolWolframAlphaToolDefinition",
    "AgentConfigToolPhotogenToolDefinition",
    "AgentConfigToolCodeInterpreterToolDefinition",
    "AgentConfigToolFunctionCallToolDefinition",
    "AgentConfigToolShield",
    "AgentConfigToolShieldMemoryBankConfig",
    "AgentConfigToolShieldMemoryBankConfigVector",
    "AgentConfigToolShieldMemoryBankConfigKeyvalue",
    "AgentConfigToolShieldMemoryBankConfigKeyword",
    "AgentConfigToolShieldMemoryBankConfigGraph",
    "AgentConfigToolShieldQueryGeneratorConfig",
]


class AgentCreateParams(TypedDict, total=False):
    agent_config: Required[AgentConfig]


class AgentConfigToolSearchToolDefinition(TypedDict, total=False):
    api_key: Required[str]

    engine: Required[Literal["bing", "brave"]]

    type: Required[Literal["brave_search"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class AgentConfigToolWolframAlphaToolDefinition(TypedDict, total=False):
    api_key: Required[str]

    type: Required[Literal["wolfram_alpha"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class AgentConfigToolPhotogenToolDefinition(TypedDict, total=False):
    type: Required[Literal["photogen"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class AgentConfigToolCodeInterpreterToolDefinition(TypedDict, total=False):
    enable_inline_code_execution: Required[bool]

    type: Required[Literal["code_interpreter"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class AgentConfigToolFunctionCallToolDefinition(TypedDict, total=False):
    description: Required[str]

    function_name: Required[str]

    parameters: Required[Dict[str, ToolParamDefinitionParam]]

    type: Required[Literal["function_call"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class AgentConfigToolShieldMemoryBankConfigVector(TypedDict, total=False):
    bank_id: Required[str]

    type: Required[Literal["vector"]]


class AgentConfigToolShieldMemoryBankConfigKeyvalue(TypedDict, total=False):
    bank_id: Required[str]

    keys: Required[List[str]]

    type: Required[Literal["keyvalue"]]


class AgentConfigToolShieldMemoryBankConfigKeyword(TypedDict, total=False):
    bank_id: Required[str]

    type: Required[Literal["keyword"]]


class AgentConfigToolShieldMemoryBankConfigGraph(TypedDict, total=False):
    bank_id: Required[str]

    entities: Required[List[str]]

    type: Required[Literal["graph"]]


AgentConfigToolShieldMemoryBankConfig: TypeAlias = Union[
    AgentConfigToolShieldMemoryBankConfigVector,
    AgentConfigToolShieldMemoryBankConfigKeyvalue,
    AgentConfigToolShieldMemoryBankConfigKeyword,
    AgentConfigToolShieldMemoryBankConfigGraph,
]

AgentConfigToolShieldQueryGeneratorConfig: TypeAlias = Union[
    DefaultQueryGeneratorConfigParam, LlmQueryGeneratorConfigParam, CustomQueryGeneratorConfigParam
]


class AgentConfigToolShield(TypedDict, total=False):
    max_chunks: Required[int]

    max_tokens_in_context: Required[int]

    memory_bank_configs: Required[Iterable[AgentConfigToolShieldMemoryBankConfig]]

    query_generator_config: Required[AgentConfigToolShieldQueryGeneratorConfig]

    type: Required[Literal["memory"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]


AgentConfigTool: TypeAlias = Union[
    AgentConfigToolSearchToolDefinition,
    AgentConfigToolWolframAlphaToolDefinition,
    AgentConfigToolPhotogenToolDefinition,
    AgentConfigToolCodeInterpreterToolDefinition,
    AgentConfigToolFunctionCallToolDefinition,
    AgentConfigToolShield,
]


class AgentConfig(TypedDict, total=False):
    instructions: Required[str]

    model: Required[str]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    sampling_params: SamplingParams

    tool_choice: Literal["auto", "required"]

    tool_prompt_format: Literal["json", "function_tag"]
    """
    `json` -- Refers to the json format for calling tools. The json format takes the
    form like { "type": "function", "function" : { "name": "function_name",
    "description": "function_description", "parameters": {...} } }

    `function_tag` -- This is an example of how you could define your own user
    defined format for making tool calls. The function_tag format looks like this,
    <function=function_name>(parameters)</function>

    The detailed prompts for each of these formats are added to llama cli
    """

    tools: Iterable[AgentConfigTool]
