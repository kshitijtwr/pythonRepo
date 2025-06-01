import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI

# from langchain.llms import OpenAI

# OPEN_AI_KEY = "SECRET_STRING""

#Upload pdf files

st.header("Welcome to Chatbot")
with st.sidebar:
    st.title("Your Documents")
    uploaded_file = st.file_uploader("Upload a PDF file and start asking questions", type="pdf")

if uploaded_file is not None:
    # Read the uploaded file
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
        # st.write(text)
        
    # Break into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    # st.write(chunks)
    
    #generating embedding
    embeddings = OpenAIEmbeddings(openai_api_key= OPEN_AI_KEY)
    
    #create vector store- FAISS
    vector_store = FAISS.from_texts(
        chunks,
        embeddings
    )
    
    #get user question
    question = st.text_input("What do you want to ask?")
    
    #do similarity search
    if question:
        match = vector_store.similarity_search(question)
        # st.write(match)
        
        #define LLM
        llm = ChatOpenAI(
            openpi_api_key = OPEN_AI_KEY,
            temperature=0,
            max_tokens=1000,
            model_name= "gpt-3.5-turbo"
        )
        
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents = match, question = question)
        st.write(response)