from prompts import build_prompt
from llm import ask_llm
from models import Document
from schemas import QuestionRequest
import pdf_handler as pdh
from text_utils import chunk_text
from vector_store import generate_embedding,load_index,create_index,save_index,add_embeddings

def query_response(qst,context):
    llm_response = ask_llm(build_prompt(context,qst))

    return llm_response

def get_pdf_text(file):
    return pdh.read_pdf(file)

def get_chunks(text):
    return chunk_text(text)

def get_embeddings(chunk):
    return generate_embedding(chunk)

def get_index(dimension,path):
    ind = load_index(path)

    if ind:
        return ind
    return create_index(dimension)

def store_index(index):
    save_index(index)

def store_embeddings(index,embds):
    add_embeddings(index,embds)