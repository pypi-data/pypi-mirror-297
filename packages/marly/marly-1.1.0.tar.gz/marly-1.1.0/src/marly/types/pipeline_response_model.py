# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.



from .._models import BaseModel

__all__ = ["PipelineResponseModel"]


class PipelineResponseModel(BaseModel):
    message: str
    """Status message"""

    task_id: str
    """Unique identifier for the pipeline task"""
