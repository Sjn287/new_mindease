from langchain_groq import ChatGroq

llm = ChatGroq(
    api_key="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",
    model_name="llama3-8b-8192"
)

response = llm.invoke("How are you?")
print(response.content)
