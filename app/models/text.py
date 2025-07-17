from pydantic import BaseModel,Field

class Text(BaseModel):
    content: str = Field(max_length=2000)