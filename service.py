from prompts import build_prompt
from llm import ask_llm
from models import Document
from schemas import QuestionRequest
import pdf_handler as pdh

def query_response(qst:QuestionRequest,docs: Document):
    llm_response = ask_llm(build_prompt(docs.content,qst.question))

    return llm_response

def get_pdf_text(file):
    return pdh.read_pdf(file)