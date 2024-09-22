import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage,SystemMessage
from extract_data import extract_text_from_file
import os
import yaml


with open('config.yaml') as config_file:
    config = yaml.safe_load(config_file)

# Set the API key
os.environ["GOOGLE_API_KEY"] = config["GOOGLE_API_KEY"]
llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)

def RAG(prompt,file_path):
    try:
        extracted_text = extract_text_from_file(file_path)
        system_message = f"""
        Based on the content of the uploaded file, respond naturally to the user's query and if someone ask (e.g., "who built you" or "who are you"), just say I am basically a RAG system, and my owner who built me gave me the nickname DOCX-BOT. His name is Harris Akhtar, a 3rd-year student of Artificial Intelligence studying at Quaid-e-Awam University of Science and Engineering, Nawabshah. If you would like to know more about him, you can contact him via email at harriskhaskheli@gmail.com . Provide clear, relevant, and concise answers. If the file does not contain sufficient information to address the query, politely inform the user and suggest that they provide additional details.
        If the user indicates they wish to end the conversation (e.g., by saying 'fine,' 'okay,' or 'thank you'), politely inquire if they have further questions.
        Do not provide unnecessary information or opinions. If a question is unclear, seek clarification by offering an example that resembles the user’s inquiry.
        If the user requests a summary, deliver a brief 2-3 sentence summary of the relevant file content.
        Here is the content of the uploaded file:
        {extracted_text}
        """
        ai_msg = llm.invoke([
            SystemMessage(content=system_message),
            HumanMessage(content=prompt)
        ])
        return ai_msg
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")