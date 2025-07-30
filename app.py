import streamlit as st
from chatbotbackend import chatbot_response  # assuming your chatbot code is saved in chatbotbackend.py

st.set_page_config(page_title="MindEase+ Chatbot", page_icon="🧠")

st.title("🧠 MindEase+ ")

st.markdown("""
Welcome to **MindEase+**, your AI companion for mental well-being.
Share how you're feeling, and I'll do my best to support you 💙
""")

# Store chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.chat_input("How are you feeling today?")

if user_input:
    # Display user's message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate chatbot response
    with st.spinner("MindEase is typing..."):
        response = chatbot_response(user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
