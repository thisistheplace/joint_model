from pydantic import BaseModel


class NpBaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
