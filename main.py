from fastapi import FastAPI,Depends,HTTPException, UploadFile, File
from database import create_tables,get_db
from sqlalchemy.orm import Session
from models import Document,DocumentChunk
from schemas import QuestionRequest
from service import get_pdf_text,query_response,get_chunks,get_embeddings,get_index,store_embeddings,store_index
from retriever import retrieve_chunks

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
        doc_text = get_pdf_text(file)
        chunks = get_chunks(doc_text)
        embeddings = [get_embeddings(i) for i in chunks]
        index = get_index(len(embeddings[0]),"vector_store/document_index.faiss")
        vector_index = index.ntotal
        store_embeddings(index,embeddings)
        store_index(index)
        new_doc = Document(
            file_name = file.filename,
            content = doc_text,
            document_chunks = [
                DocumentChunk(
                    chunk_text = chunk,
                    vector_id = vector_index + idx
                )
                for idx,chunk in enumerate(chunks)
            ]
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)
        return {
            "id":new_doc.id,
            "file_name":new_doc.file_name,
            "characters": len(new_doc.content),
            "no_of_chunks": len(new_doc.document_chunks)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.post("/ask")
def ask_llm(question:QuestionRequest,db:Session=Depends(get_db)):
    vector_ids = retrieve_chunks(question.question)
    doc = db.query(DocumentChunk).filter(
        DocumentChunk.vector_id.in_(vector_ids)
    ).all()
    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Document or relevant chunks not found"
        )
    
    try:
        context = ''
        sources = set()
        for i in doc:
            context += i.chunk_text + '\n'
            sources.add(i.document.file_name)
        output = query_response(question.question,context)
        return {
            "answer":output,
            "sources":list(sources)
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