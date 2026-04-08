from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(..., example="What is this document about?")
    top_k: int = Field(3, example=3)