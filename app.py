import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from textblob import TextBlob
from dotenv import load_dotenv

load_dotenv()

# Setup LLM
llm = ChatGroq(
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192"
)

# Create chatbot prompt
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

# Sentiment analysis setup
def detect_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity < -0.2:
        return "negative"
    elif polarity > 0.2:
        return "positive"
    else:
        return "neutral"


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
    # 1. First check rule-based FAQs
    faq_reply = rule_based_response(user_input)
    if faq_reply:
        return faq_reply

    # 2. Safety Filter for crisis-related inputs
    crisis_keywords = [
        'suicide', 'kill myself', 'want to die', 'end my life',
        'cutting', 'self-harm', 'depressed', 'hopeless', 'overwhelmed'
    ]
    if any(keyword in user_input.lower() for keyword in crisis_keywords):
        return (
            "💙 I'm really sorry you're feeling this way. You're not alone.\n\n"
            "**Please consider reaching out to a professional or support line:**\n"
            "- **India (iCall): +91 9152987821**\n"
            "- **AASRA (Mumbai): +91 9820466726**\n"
            "- **International Help:** https://www.befrienders.org\n\n"
            "You matter, and support is available. 💙"
        )

    # 3. Sentiment Detection
    mood = detect_sentiment(user_input)
    if mood == "negative":
        user_input = "User is feeling low. Respond with extra empathy. Keep the response under 100 words.\n" + user_input

    # 4. Final LLM Response
    response = chain.invoke({"user_input": user_input}).content

    # 5. Length check – fallback to short, empathetic version
    if len(response) > 400:
        return get_short_response()

    return response


# Example usage
user_message = "I am sad"
chatbot_response(user_message)