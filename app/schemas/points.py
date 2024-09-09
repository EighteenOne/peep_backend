from pydantic import BaseModel, Field


class PointInput(BaseModel):
    point: str = Field(min_length=1, max_length=120)
    key: str
