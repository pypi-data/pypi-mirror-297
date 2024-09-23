# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable
from typing_extensions import Required, TypedDict

__all__ = ["PipelineCreateParams", "Workload"]


class PipelineCreateParams(TypedDict, total=False):
    api_key: Required[str]
    """API key for the AI provider"""

    provider_model_name: Required[str]
    """Name of the AI model to use"""

    provider_type: Required[str]
    """Type of AI provider (e.g., 'azure', 'openai')"""

    workloads: Required[Iterable[Workload]]
    """Array of workload objects containing PDF content and schemas"""

    additional_params: Dict[str, object]
    """Additional parameters specific to the AI provider"""

    markdown_mode: bool
    """Flag to enable markdown mode"""


class Workload(TypedDict, total=False):
    pdf_stream: Required[str]
    """Base64 encoded and zlib compressed PDF content"""

    schemas: Required[List[str]]
    """JSON strings representing extraction schemas"""
