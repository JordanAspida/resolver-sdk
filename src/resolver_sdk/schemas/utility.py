"""
Pydantic models for Utility API responses.
"""
from .base import BaseResolverModel
from pydantic import Field
from typing import Any

# Job Response schema to map the output when polling for a job
class JobResponse(BaseResolverModel):
    jobId : str = Field(alias="id")
    status : int
    payload : dict[Any, Any] = Field(default_factory=dict) # will be {} until job has executed in which case it will show the response of whatever action was being executed
    started : int
    finished : int | None = None
    metadata : dict[Any, Any] = Field(default_factory=dict) # not sure what goes here have only seen it empty as {}