import os
import traceback
from dotenv import load_dotenv
from textblob import TextBlob
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Load from .env if not hardcoding (recommended)
load_dotenv()

# Initialize Groq LLM safely
try:
    llm = ChatGroq(
        api_key= "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",
        model_name="llama3-8b-8192",
        temperature=0.5
    )
except Exception as init_error:
    print("[ERROR] Failed to initialize LLM:", init_error)
    llm = None

# Prompt Template
template = PromptTemplate.from_template("""
You are MindEase+, a supportive and compassionate mental health companion.
Listen to the user, understand their emotions, and provide empathetic responses and helpful advice.

User: {question}
MindEase+:
""")

# Rule-based response
def rule_based_response(query):
    q = query.lower()
    if "emergency" in q or "suicide" in q:
        return "⚠️ If this is an emergency, please contact a mental health professional or your local emergency number immediately."
    if "hello" in q or "hi" in q:
        return "Hello there! I'm MindEase+, your mental wellness companion. How can I support you today?"
    if "thank you" in q or "thanks" in q:
        return "You're always welcome 💙"
    return None

# Main chatbot function
def chatbot_response(query):
    try:
        print(f"[DEBUG] Received query: {query}")

        if len(TextBlob(query).words) < 2:
            return "Could you please tell me a bit more so I can help you better?"

        rule_reply = rule_based_response(query)
        if rule_reply:
            print("[DEBUG] Rule-based response matched.")
            return rule_reply

        if not llm:
            print("[ERROR] LLM not initialized.")
            return "⚠️ I'm having trouble connecting to my brain. Please try again later."

        prompt = template.format(question=query)
        print(f"[DEBUG] Sending to LLM: {prompt}")
        response = llm.invoke(prompt)

        if not response or not response.content.strip():
            print("[ERROR] LLM returned empty response.")
            return "I'm really sorry, but I didn't understand that. Can you rephrase it?"

        print(f"[DEBUG] LLM response: {response.content.strip()}")
        return response.content.strip()

    except Exception as e:
        print("[FATAL ERROR] Exception during response generation:")
        traceback.print_exc()
        return "Sorry, an unexpected error occurred. Please try again later."
