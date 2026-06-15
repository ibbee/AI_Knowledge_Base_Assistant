from fastapi import FastAPI,Depends,HTTPException
from database import create_tables,get_db
from sqlalchemy.orm import Session
from schemas import DocumentCreate
from models import Document

app = FastAPI()

create_tables()

@app.get('/')
def default():
    return {'message':'AI Knowledge Base Assistant is Running'}

@app.get('/documents')
def get_documents(db:Session = Depends(get_db)):
    docs = db.query(Document).all()
    return {
        "documents": [
            {
                "id": doc.id,
                "file_name": doc.file_name,
                "upload_date": doc.upload_date
            }
            for doc in docs
        ]
    }

@app.post('/documents')
def insert_documents(data:DocumentCreate,db:Session=Depends(get_db)):
    new_doc = Document(
        file_name = data.file_name
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return {
        "id":new_doc.id,
        "file_name":new_doc.file_name,
        "upload_date":new_doc.upload_date
    }

@app.delete("/documents/{doc_id}")
def delete_document(doc_id:int,db:Session=Depends(get_db)):
    doc = db.query(Document).filter(
        Document.id == doc_id
    ).first()

    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    
    db.delete(doc)
    db.commit()

    return {
        "message": "Document deleted successfully",
        "deleted_document": {
            "id": doc.id,
            "file_name": doc.file_name
        }
    }