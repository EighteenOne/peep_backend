from pydantic import BaseModel, PositiveInt, Field, EmailStr, PastDate


class TemplateInput(BaseModel):
    point: str = Field(min_length=1, max_length=120)
    template_text: str
    subject: str = Field(min_length=1, max_length=120)
