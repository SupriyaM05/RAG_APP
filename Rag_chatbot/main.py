import os
import PyPDF2
import streamlit as st
from google.generativeai import GenerativeModel
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import TextSplitter, CharacterTextSplitter
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS

ROOT_PATH= os.path.abspath(os.path.dirname(__file__))
EMBEDDINS_PATH= os.path.join(ROOT_PATH, 'embeddings')

load_dotenv()

embeddings_model = GoogleGenerativeAIEmbeddings(model= 'models/embedding-001', google_api_key= os.getenv('GOOGLE_API_KEY'))

st.set_page_config('RAG based Chatbot Application', layout='wide')
st.title('RAG based Chatbot Application')

with st.sidebar:
    file_uploader = st.file_uploader(label='Upload pdf documents', accept_multiple_files=True)

    if file_uploader:
        text= ''
        for _file in file_uploader:
            file_name = _file.name
            reader= PyPDF2.PdfReader(_file)
            pages=reader.pages
            
            for page in pages:
                text += page.extract_text()

        text_splitter= chunks = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
        chunks= text_splitter.split_text(text)

        if st.button('Calculate Embeddings'):
            with st.spinner():
                vector_store= FAISS.from_texts(chunks, embeddings_model)
            if os.path.exists(EMBEDDINS_PATH):
                vector_store.save_local(os.path.join(EMBEDDINS_PATH, 'vector_store'))
                st.success('Vector Store saved successfully for thr pdf')

st.divider()





