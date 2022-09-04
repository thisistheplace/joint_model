from enum import Enum
from pathlib import Path
import uuid

class JobStatus(Enum):
    PENDING = 1
    RUNNING = 2
    COMPLETE = 3
    ERROR = 4

class Job:
    def __init__(self, data):
        self._id = str(uuid.uuid4())
        self._data = data
        self._error = None
        self._path = Path(self.id).resolve() / "mesh.mesh"
        self._status = JobStatus.PENDING

    @property
    def id(self) -> str:
        return self._id

    @property
    def data(self):
        return self._data

    @property
    def error(self) -> str:
        return self._error

    @error.setter
    def error(self, value: str):
        self.status = JobStatus.ERROR
        self._error = value

    @property
    def path(self) -> Path:
        return self._path

    @property
    def status(self) -> JobStatus:
        return self._status

    @status.setter
    def status(self, value: JobStatus):
        self._status = value
    
