import os
import logging
from dotenv import load_dotenv
from textblob import TextBlob
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(filename="chatbot_logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# Initialize Groq LLaMA3 model
llm = ChatGroq(
    api_key="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",
    temperature=0.5,
    model_name="llama3-8b-8192"
)

# Define prompt template
template = PromptTemplate.from_template("""
You are MindEase, a caring, intelligent, and helpful mental health assistant.
Always reply to the user's message with empathy, support, and helpful guidance.
Provide real, informative, and non-repetitive answers.

User: {question}
MindEase:
""")

# Rule-based quick response system
def rule_based_response(query):
    q = query.lower()

    if any(word in q for word in ["emergency", "suicide", "urgent", "immediately"]):
        return "⚠️ If you're in an emergency or experiencing suicidal thoughts, please contact a mental health professional or call your country's emergency number immediately. You're not alone."

    if "hello" in q or "hi" in q:
        return "Hello! I'm MindEase 😊. How can I support you today?"

    if "thank you" in q or "thanks" in q:
        return "You're always welcome. I'm here for you anytime 💛."

    if "who are you" in q:
        return "I'm MindEase, your AI-powered mental wellness companion, here to support your emotional well-being."

    return None  # No rule matched

# Check if the question is valid
def is_valid_query(query):
    blob = TextBlob(query)
    return len(blob.words) >= 2

# Generate response from LLM
def generate_llm_response(query):
    prompt = template.format(question=query)
    return llm.invoke(prompt).content.strip()

# Main chatbot response function
def chatbot_response(query):
    try:
        query = query.strip()
        if not is_valid_query(query):
            return "Could you please provide more context or details so I can better assist you?"

        # Check rule-based answers
        rule_response = rule_based_response(query)
        if rule_response:
            return rule_response

        # Query LLM
        llm_response = generate_llm_response(query)

        # If LLM responds poorly, use fallback
        if not llm_response or "I don’t understand" in llm_response.lower():
            return "I'm here to help, but I didn’t fully understand that. Could you rephrase or explain a bit more?"

        # Log successful query
        logging.info(f"User Query: {query}\nBot Reply: {llm_response}\n")
        return llm_response

    except Exception as e:
        logging.error(f"Error processing query: {query} | Error: {str(e)}")
        return "I'm facing a temporary issue understanding your request. Please try again shortly."

