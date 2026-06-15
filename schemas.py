from pydantic import BaseModel

class DocumentCreate(BaseModel):
    file_name: str