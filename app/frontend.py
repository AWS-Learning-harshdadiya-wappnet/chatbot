import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"  # 🔁 Change this to your deployed App Runner URL

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("🧠 Mini Chatbot using Groq + OpenAI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", "", placeholder="Say something...")
    submitted = st.form_submit_button("Send")
    if submitted and user_input.strip():
        try:
            res = requests.post(API_URL, json={"message": user_input})
            res.raise_for_status()
            reply = res.json().get("reply", "⚠️ No reply")
        except Exception as e:
            reply = f"❌ Error: {e}"
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", reply))

# Show conversation history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)
