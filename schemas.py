from pydantic import BaseModel

class DocumentCreate(BaseModel):
    file_name: str
    content: str

class QuestionRequest(BaseModel):
    question: str