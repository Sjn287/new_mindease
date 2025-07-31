
import random
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from textblob import TextBlob
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(
    temperature=0.7,
    api_key="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",
    model_name="llama3-8b-8192"
)


prompt = PromptTemplate.from_template(
    """
    You are MindEase, a CBT-based AI therapist trained to support users facing stress, anxiety, and emotional challenges.

    ### USER INPUT:
    {user_input}

    ### INSTRUCTION:
    Be warm, encouraging, non-robotic. Ask questions when helpful. Use CBT techniques like reframing, grounding, or journaling. Keep responses under 120 words unless otherwise required.
    """
)
chain = prompt | llm


def detect_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity < -0.1:
        return "negative"
    elif polarity > 0.1:
        return "positive"
    else:
        return "neutral"


faq = {
    "i feel stressed": "It's okay to feel this way. Try taking deep breaths or journaling your thoughts.",
    "how to deal with anxiety": "Start with grounding techniques like 5-4-3-2-1. Want help trying one?",
    "i can't sleep": "Avoid screens before bed, try calming sounds or deep breathing exercises."
}

def rule_based_response(user_input):
    for key in faq:
        if key in user_input.lower():
            return faq[key]
    return None


def check_crisis_keywords(text):
    crisis_keywords = ['suicide', 'kill myself', 'want to die', 'end my life', 'cutting', 'self-harm']
    return any(keyword in text.lower() for keyword in crisis_keywords)


def get_short_response():
    responses = [
        "I'm here for you. It's okay to feel this way — you're not alone. 💙",
        "Thanks for opening up. Want to talk more about what's on your mind?",
        "I'm really sorry you're feeling this way. Let's get through it together. 🌱",
        "Take a deep breath — I'm with you. What happened recently that made you feel like this?"
    ]
    return random.choice(responses)


def get_positive_response():
    responses = [
        "That's wonderful! Keep riding that wave of joy! 🌟",
        "Love hearing that! What made your day so good?",
        "That's amazing! Hold onto that feeling and share it with others. 💛",
        "You're glowing with positivity — keep shining! ✨"
    ]
    return random.choice(responses)


def get_neutral_response():
    responses = [
        "Thanks for sharing. Would you like to explore how you're feeling more deeply?",
        "It sounds like a balanced day. Want to reflect on something that stood out?",
        "I'm here if you want to talk or unwind a bit.",
        "Not every day has to be eventful. What’s something small that brought you peace?"
    ]
    return random.choice(responses)


def chatbot_response(user_input):

    faq_reply = rule_based_response(user_input)
    if faq_reply:
        return faq_reply


    if check_crisis_keywords(user_input):
        return (
            "💙 I'm really sorry you're feeling this way. You're not alone.\n\n"
            "**Please consider reaching out to a professional or support line:**\n"
            "- **India (iCall): +91 9152987821**\n"
            "- **AASRA (Mumbai): +91 9820466726**\n"
            "- **International Help:** https://www.befrienders.org\n\n"
            "You matter, and help is available. 💙"
        )

    mood = detect_sentiment(user_input)

    if mood == "positive":
        return get_positive_response()

    elif mood == "neutral":
        if random.random() < 0.5:
            return get_neutral_response()

    elif mood == "negative":
        user_input = "User is feeling low. Respond empathetically and with care. Be warm and comforting.\n" + user_input

    response = chain.invoke({"user_input": user_input}).content.strip()

    if len(response) > 400 and mood == "negative":
        return get_short_response()

    return response


# ✅ Example usage
if __name__ == "__main__":
    while True:
        user_message = input("\nYou: ")
        if user_message.lower() in ["exit", "quit"]:
            break
        bot_reply = chatbot_response(user_message)
        print("\nMindEase:", bot_reply)
