from fastapi import FastAPI,Depends,HTTPException, UploadFile, File
from database import create_tables,get_db
from sqlalchemy.orm import Session
from models import Document
from schemas import QuestionRequest
from service import get_pdf_text,query_response

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
                "upload_date": doc.upload_date,
                "characters": len(doc.content)
            }
            for doc in docs
        ]
    }

@app.post('/documents/upload')
def insert_documents(file: UploadFile =File(...),db:Session=Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file format, only PDF is allowed."
        )
    try:
        new_doc = Document(
            file_name = file.filename,
            content = get_pdf_text(file)
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)
        return {
            "id":new_doc.id,
            "file_name":new_doc.file_name,
            "characters": len(new_doc.content)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.post("/ask")
def ask_llm(question:QuestionRequest,db:Session=Depends(get_db)):
    doc = db.query(Document).filter(
        Document.id == question.document_id
    ).first()

    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    
    try:
        output = query_response(question,doc)
        return {
            "answer":output
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

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