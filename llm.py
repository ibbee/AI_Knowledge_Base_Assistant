import ollama

def ask_llm(prompt):
    response = ollama.chat(
        model="mistral:latest",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response["message"]["content"]