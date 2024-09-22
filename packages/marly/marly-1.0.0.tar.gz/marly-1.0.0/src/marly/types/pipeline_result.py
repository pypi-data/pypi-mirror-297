# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["PipelineResult", "Result"]


class Result(BaseModel):
    metrics: Dict[str, str]
    """Metrics related to the schema extraction"""

    schema_data: Dict[str, str]
    """Extracted data based on the schema"""

    schema_id: str
    """Identifier for the schema used"""


class PipelineResult(BaseModel):
    results: List[Result]
    """Array of schema results"""

    status: Literal["PENDING", "IN_PROGRESS", "COMPLETED", "FAILED"]
    """Current status of the pipeline job"""

    task_id: str
    """Unique identifier for the pipeline task"""

    total_run_time: str
    """Total execution time of the pipeline"""
