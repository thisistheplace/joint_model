from pydantic import BaseModel

from .job import JobStatus

class MeshJob(BaseModel):
    id: str = ...
    status: JobStatus = ...