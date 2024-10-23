from pydantic import BaseModel, PositiveInt, Field, EmailStr, NonNegativeInt


class SessionInput(BaseModel):
    count_photos: NonNegativeInt
    datetime_str: str = Field(min_length=1, max_length=21)
    email: EmailStr
    name: str = Field(min_length=1, max_length=120)
    point: str = Field(min_length=1, max_length=120)
    session: str = Field(min_length=1, max_length=120)
    status: int


class CreateSessionInput(BaseModel):
    datetime_str: str = Field(min_length=1, max_length=21)
    email: EmailStr
    name: str = Field(min_length=1, max_length=120)
    point: str = Field(min_length=1, max_length=120)
    session: str = Field(min_length=1, max_length=120)


class CloseSessionInput(BaseModel):
    point: str = Field(min_length=1, max_length=120)
    session: str = Field(min_length=1, max_length=120)
    count_photos: PositiveInt


class GetWaitingSessionsInput(BaseModel):
    point: str = Field(min_length=1, max_length=120)


class GetWaitingSessionsOutput(BaseModel):
    session: str = Field(min_length=1, max_length=120)
    disk_path: str = Field(min_length=1, max_length=120)
    datetime_str: str = Field(min_length=1, max_length=21)
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr


class SessionOutput(SessionInput):
    id: str

    status: int
    count_photos_cloud: int
    public_link: str
