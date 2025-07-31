import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from textblob import TextBlob

# Use API key directly for testing (do NOT do this in production)
api_key = "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"

# Setup LLM
llm = ChatGroq(
    temperature=0.7,
    api_key=api_key,
    model_name="llama3-8b-8192"
)

# Prompt template
prompt = PromptTemplate.from_template(
    """
    You are MindEase, a CBT-based AI therapist trained to support users facing stress, anxiety, and overthinking.

    ### USER INPUT:
    {user_input}

    ### INSTRUCTION:
    Gently ask guiding questions, reflect emotions, and suggest techniques such as journaling, grounding, or reframing thoughts.
    Be warm, helpful, and avoid sounding robotic.
    """
)
chain = prompt | llm

# Sentiment detection
def detect_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity < -0.2:
        return "negative"
    elif polarity > 0.2:
        return "positive"
    return "neutral"

# Rule-based responses
faq = {
    "i feel stressed": "It's okay to feel this way. Try taking deep breaths or journaling your thoughts.",
    "how to deal with anxiety": "Start with grounding techniques like 5-4-3-2-1. Would you like more suggestions?",
    "i can't sleep": "Avoid screens at night, try calming music, or practice deep breathing exercises."
}

def rule_based_response(user_input):
    for key in faq:
        if key in user_input.lower():
            return faq[key]
    return None

def get_short_response():
    return (
        "I'm really sorry you're feeling this way. It's okay to feel sad, and you're not alone.\n\n"
        "I'm here to listen — would you like to share what's been on your mind lately?\n\n"
        "Sometimes writing down your thoughts can help bring a little clarity. If you're open to it, we can explore what you're feeling together.\n\n"
        "You're doing your best, and that matters. 💙"
    )

def chatbot_response(user_input):
    try:
        # 1. Rule-based reply
        faq_reply = rule_based_response(user_input)
        if faq_reply:
            return faq_reply

        # 2. Safety Filter
        crisis_keywords = [
            'suicide', 'kill myself', 'want to die', 'end my life',
            'cutting', 'self-harm', 'depressed', 'hopeless', 'overwhelmed'
        ]
        if any(keyword in user_input.lower() for keyword in crisis_keywords):
            return (
                "💙 I'm really sorry you're feeling this way. You're not alone.\n\n"
                "*Please consider reaching out to a professional or support line:*\n"
                "- *India (iCall): +91 9152987821*\n"
                "- *AASRA (Mumbai): +91 9820466726*\n"
                "- *International Help:* https://www.befrienders.org\n\n"
                "You matter, and support is available. 💙"
            )

        # 3. Sentiment detection
        mood = detect_sentiment(user_input)
        if mood == "negative":
            user_input = "User is feeling low. Respond with extra empathy. Keep the response under 100 words.\n" + user_input

        # 4. LLM response
        response_obj = chain.invoke({"user_input": user_input})
        if not response_obj or not hasattr(response_obj, 'content'):
            return get_short_response()

        response = response_obj.content.strip()
        if len(response) > 400:
            return get_short_response()

        return response

    except Exception as e:
        st.error(f"[ERROR]: {str(e)}")
        return "Sorry, I'm having trouble responding right now. Please try again shortly."

# Streamlit interface
st.title("🧠 MindEase - Mental Health Chatbot")
user_input = st.text_input("How are you feeling today?")

if user_input:
    reply = chatbot_response(user_input)
    st.write("💬", reply)
