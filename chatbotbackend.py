import streamlit as st
from textblob import TextBlob
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# === Initialize ChatGroq LLM ===
llm = ChatGroq(
    temperature=0.7,
    api_key="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",
    model_name="llama3-8b-8192"
)

# === Prompt Template ===
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

# === Sentiment Analysis ===
def detect_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity < -0.2:
        return "negative"
    elif polarity > 0.2:
        return "positive"
    return "neutral"

# === Rule-Based Responses ===
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
    faq_reply = rule_based_response(user_input)
    if faq_reply:
        return faq_reply

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

    if detect_sentiment(user_input) == "negative":
        user_input = "User is feeling low. Respond with extra empathy. Keep the response under 100 words.\n" + user_input

    response = chain.invoke({"user_input": user_input}).content

    if len(response) > 400:
        return get_short_response()

    return response

# === Streamlit UI ===
st.set_page_config(page_title="MindEase - Mental Health Chatbot", layout="centered", page_icon="🧠")

st.markdown("## 🧠 MindEase - Mental Health Chatbot")
st.markdown("How are you feeling today?")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    role = "🧑‍💬 You" if message["role"] == "user" else "🤖 MindEase"
    st.markdown(f"**{role}:** {message['content']}")

# Input box
user_input = st.text_input("Your message", label_visibility="collapsed")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_reply = chatbot_response(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_reply})
    st.experimental_rerun()
