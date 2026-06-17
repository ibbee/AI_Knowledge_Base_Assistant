from pydantic import BaseModel

class DocumentCreate(BaseModel):
    file_name: str
    content: str

class QuestionRequest(BaseModel):
    document_id: int
    question: str