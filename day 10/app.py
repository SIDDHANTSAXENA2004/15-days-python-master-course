import streamlit as st
import requests

st.title("my full stack ai chat app")

user_prompt=st.text_area("")
API_URL="http://127.0.0.1:8000/ask-ai"
if st.button("send"):
    payload={
        "text":user_prompt
    }


    with st.spinner("ai is thinking..."):
         try:
             response=requests.post(API_URL,json=payload)

             if response.status_code==200:
                response_data=response.json()
                st.subheader("ai response : ")
                
                st.write(response_data["ai_response"])
             else:
                st.error(f"error from api server {response.status_code}- {response.text}")
         except requests.exceptions.ConnectionError:
             st.error("Please make sure the api server is running")


        

