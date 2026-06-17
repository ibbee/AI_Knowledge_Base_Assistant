def build_prompt(context,question):
    prompt = f'''
You are a helpful assistant.

Answer ONLY using the provided document content.

If the answer is not present in the document, reply:

"I don't know based on the uploaded documents."

Document Content:
{context}

Question:
{question}
'''
    return prompt