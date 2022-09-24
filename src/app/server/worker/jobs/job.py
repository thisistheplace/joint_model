from enum import Enum
import uuid

from ....interfaces import DashVtkModel, Model


class JobStatus(str, Enum):
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"
    NOTFOUND = "NOTFOUND"


class Job:
    def __init__(self, model: Model, id: str | None = None):
        if id is None:
            self._id = str(uuid.uuid4())
        else:
            self._id = id
        self._data = model
        self._mesh = None
        self._error = None
        self._status = JobStatus.PENDING

    @property
    def id(self) -> str:
        return self._id

    @property
    def data(self) -> Model:
        return self._data

    @property
    def error(self) -> str:
        return self._error

    @error.setter
    def error(self, value: str):
        self.status = JobStatus.ERROR
        self._error = value

    @property
    def mesh(self) -> DashVtkModel:
        return self._mesh

    @mesh.setter
    def mesh(self, value: DashVtkModel):
        self._mesh = value

    @property
    def status(self) -> JobStatus:
        return self._status

    @status.setter
    def status(self, value: JobStatus):
        self._status = value

    def __str__(self):
        return f"id: {self.id}\nstatus: {self.status}\nerror: {self.error}"
