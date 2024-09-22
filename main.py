import RAG
import streamlit as st
import os
from extract_data import doc_info, extract_text_from_file
from fpdf import FPDF

st.set_page_config(page_title="RAG_SYSTEM", layout="centered", initial_sidebar_state="expanded")

st.markdown("""
    <div style="display: flex; align-items: center;">
        <h1 style="margin-right: 20px;">DOCX-BOT:</h1>
        <img src="https://img.freepik.com/free-vector/cartoon-style-robot-vectorart_78370-4103.jpg?w=740&t=st=1726496426~exp=1726497026~hmac=a0a105a9b0d48986bf0c79465a47bb245fbd942a31022029288d102531e47e40" alt="DOCX-BOT Image" style="width: 80px; height: auto;">
    </div>
    """, unsafe_allow_html=True)

st.markdown("Please upload document to continue")

# CSS for chat style
st.markdown("""
<style>
.message { margin-bottom: 10px; display: flex; align-items: flex-start; gap: 10px; }
.user-message, .bot-message { padding: 10px 15px; border-radius: 15px; max-width: 80%; word-wrap: break-word; font-size: 16px; }
.user-message { background-color: #007bff; color: white; margin-left: auto; text-align: right; }
.bot-message { margin-top: 15px; background-color: #f1f0f0; color: black; text-align: left; margin-bottom: 15px; }
.bot-avatar { margin-top: 15px; width: 40px; height: 40px; border-radius: 50%; object-fit: cover; margin-right: 10px; }
.bot-container { display: flex; align-items: top; gap: 10px; }
.user-container { display: flex; justify-content: flex-end; }
</style>
""", unsafe_allow_html=True)

# Ensure chat history exists in session state
if 'chat_sessions' not in st.session_state:
    st.session_state.chat_sessions = []

DOCUMENT_UPLOADED = False
# File uploader
uploaded_file = st.file_uploader("Upload a file", type={'txt', 'csv', 'json', 'pdf', 'docx'})

if uploaded_file:
    # Save uploaded file
    upload_dir = 'uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    file_path = os.path.join(upload_dir, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    # Process document and update metadata
    extracted_content = extract_text_from_file(file_path)
    DOCUMENT_UPLOADED = True

# Sidebar
with st.sidebar:
    if DOCUMENT_UPLOADED:
        data = doc_info()  # Get updated document metadata
        st.markdown('---------------DOCUMENT DETAILS---------------')
        st.markdown('_______________________________________________')
        st.markdown(f"DOCUMENT TYPE : {data['Document Type']}")
        st.markdown(f"DOCUMENT SIZE : {data['Document Size (bytes)']}")
        st.markdown(f"DOCUMENT PAGES : {data['Document Pages']}")
        st.markdown(f"DOCUMENT LINES : {data['Document Lines']}")
        st.markdown(f"DOCUMENT WORDS : {data['Document Words']}")
        st.markdown('---')

        # Add a button for downloading the conversation as a PDF
        if st.button("Generate PDF of Conversation"):
            # Generate PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Conversation History", ln=True, align='C')
            pdf.ln(10)  # Add a line break

            for chat in st.session_state.chat_sessions:
                user_input = f"Q: {chat['input']}"
                bot_response = f"A: {chat['response']}"

                pdf.multi_cell(0, 10, user_input)
                pdf.multi_cell(0, 10, bot_response)
                pdf.ln(5)  # Add some space between conversations

            # Save the PDF to a file
            pdf_output_path = os.path.join(upload_dir, "chat_conversation.pdf")
            pdf.output(pdf_output_path)

            # Provide the file for download immediately
            with open(pdf_output_path, "rb") as pdf_file:
                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name="chat_conversation.pdf",
                    mime="application/pdf"
                )

    else:
        st.markdown("No document uploaded.")

# Chat interaction
if DOCUMENT_UPLOADED:
    prompt = st.chat_input("Say something", key="unique_chat_input_key")
    if prompt:
        ai_msg = RAG.RAG(prompt, file_path)
        # Store the chat in session state
        st.session_state.chat_sessions.append({
            'input': prompt,
            'response': ai_msg.content
        })

# Display conversation history after the form is submitted
if st.session_state.chat_sessions:
    for chat in st.session_state.chat_sessions:
        st.markdown(f'<div class="user-container"><div class="user-message">{chat["input"]}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bot-container"><img src="https://img.freepik.com/free-vector/cartoon-style-robot-vectorart_78370-4103.jpg?w=740&t=st=1726496426~exp=1726497026~hmac=a0a105a9b0d48986bf0c79465a47bb245fbd942a31022029288d102531e47e40" class="bot-avatar"/><div class="bot-message">{chat["response"]}</div></div>', unsafe_allow_html=True)
