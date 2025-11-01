import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/query"

st.title("Document Chatbot")
st.write("Ask questions about your documents like webscraping.txt and oops_java.pdf")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:=st.chat_input("Ask me anything ..."):
    st.session_state.messages.append({"role": "human", "content": prompt})
    with st.chat_message("human"):
        st.markdown(prompt)
    
    with st.chat_message("ai"):
        with st.spinner("Thinking ..."):
            
            try:
                res=requests.post(API_URL, json={"text": prompt})
                res.raise_for_status()
                answer=res.json()["answer"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "ai", "content": answer})
            except Exception as e:
                st.error(f"api error {e}")
                