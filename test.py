import streamlit as st
import os
import pdfplumber
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS


# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# Streamlit web app
def main():
    
    # st.title("Document Text to FAISS Vector Database")
    # uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

    # if uploaded_file is not None:
    #     file_extension = os.path.splitext(uploaded_file.name)[1]
    #     if file_extension == ".pdf":
    #         text = extract_text_from_pdf(uploaded_file)
    #     elif file_extension == ".docx":
    #         text = extract_text_from_docx(uploaded_file)
        
    #     store_text_in_faiss_index(text)
    #     st.success("Text vector stored in FAISS index!")
        
    with st.sidebar:
        st.title("Menu:")
        # pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button",type=['.pdf','.docx'],accept_multiple_files=True)
        pdf_docs = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"],accept_multiple_files=True) 
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
             if pdf_docs is not None:
                for uploaded_file in pdf_docs:
                    file_extension = os.path.splitext(uploaded_file.name)[1]
                if file_extension == ".pdf":
                    text = extract_text_from_pdf(uploaded_file)
                elif file_extension == ".docx":
                    text = extract_text_from_docx(uploaded_file)
                    
                text_chunks = get_text_chunks(text)
                get_vector_store(text_chunks)
                st.success("Done")    

if __name__ == "__main__":
    main()