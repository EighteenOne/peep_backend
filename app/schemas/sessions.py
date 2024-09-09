from pydantic import BaseModel, PositiveInt, Field, EmailStr, PastDate


class SessionInput(BaseModel):
    count_photos: PositiveInt
    datetime_str: str = Field(min_length=1, max_length=21)
    email: EmailStr
    name: str = Field(min_length=1, max_length=120)
    point: str = Field(min_length=1, max_length=120)
    session: str = Field(min_length=1, max_length=120)


class SessionOutput(SessionInput):
    id: str

    status: int
    count_photos_cloud: int
    public_link: str
