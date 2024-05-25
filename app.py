import streamlit as st
from dotenv import load_dotenv
import pypdfium2 as pdfium
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceInstructEmbeddings
from langchain.vectorstores.faiss import FAISS
import requests
import os
from together import Together

from htmlTemplates import css, bot_template, user_template

def get_pdf_text(pdf_docs):
    text = " "
    for pdf in pdf_docs:
        pdf_reader= pdfium.PdfDocument(pdf)
        for i in range(len(pdf_reader)):
            page= pdf_reader.get_page(i)
            textpage= page.get_textpage()
            text += textpage.get_text_range() + "/n"
        return text
            
def get_text_chunk(text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=5000, chunk_overlap=500, length_function=len)   
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="BAAI/bge-large-en-v1.5")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

together_ai_endpoint = "https://api.together.xyz/v1/chat/completions"
def generate_conversation_response(question):
    together_ai_api_key = os.getenv("TOGETHER_AI_API_KEY")  # Ensure API key is set
    if together_ai_api_key is None:
        raise ValueError("TOGETHER_AI_API_KEY environment variable not set")

    data = {
        "question": question,
        "model": "mistralai/Mixtral-8x7B-v0.1"
    }
    headers = {
        "Authorization": f"Bearer {together_ai_api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(together_ai_endpoint, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return "Failed to generate response."

def save_question_and_clear_prompt(ss):
    ss.user_question = ss.prompt_bar
    
    ss.prompt_bar = ""  # clearing the prompt bar after clicking enter to prevent automatic re-submissions
        
def write_chat(msgs):  # Write the Q&A in a pretty chat format
        for i, msg in enumerate(msgs):
            if i % 2 == 0:  # it's a question
                 st.write(user_template.replace("{{MSG}}", msg["content"]), unsafe_allow_html=True)
            else:  # it's an answer
                st.write(bot_template.replace("{{MSG}}", msg["content"]), unsafe_allow_html=True)
    
def main():
    load_dotenv()
    ss = st.session_state
    
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    st.header("Chat with Multiple PDFs :books:")
    
    
    # Initializing session state variables
    if "prompt_bar" not in ss:
        ss.prompt_bar = ""
    if "user_question" not in ss:
        ss.user_question = ""
    if "docs_are_processed" not in ss:
        ss.docs_are_processed = False
    
    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("Upload your documentation here, then click 'Process' ", accept_multiple_files=True, type="pdf")
        if st.button("Process") and pdf_docs:    
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)  # get pdf text
                text_chunks = get_text_chunk(raw_text)  # get text chunks
                vectorstore = get_vectorstore(text_chunks)  # create vectorstore
                ss.vectorstore = vectorstore  # store vectorstore in session state
                ss.docs_are_processed = True
        if ss.docs_are_processed:
            st.success("Documents Processed")
            
    st.text_input("Ask a question :", key="prompt_bar", on_change=save_question_and_clear_prompt(ss))

    
    if ss.user_question:
        response = generate_conversation_response(ss.user_question)  # fetch response from Together AI
        chat = [{'content': ss.user_question}, {'content': response}]  # format response
        write_chat(chat)
    
    # st.write(ss)       
    
if __name__ == '__main__' :
    together_ai_api_key = os.getenv("TOGETHER_AI_API_KEY")
    if together_ai_api_key is None:
        raise ValueError("TOGETHER_AI_API_KEY environment variable not set")
    main()
