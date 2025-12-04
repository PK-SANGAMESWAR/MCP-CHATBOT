import streamlit as st
import asyncio
from backend import run_agent   

st.set_page_config(page_title="MCP Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 MCP-Powered Chatbot")
st.write("Chat with Math, Expense, and Manim MCP tools.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# Chat input
prompt = st.chat_input("Ask anything...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Run backend agent
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.write("Thinking... ⏳")

        # Run async backend call
        reply = asyncio.run(run_agent(prompt))

        placeholder.write(reply)

    # Save bot reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
