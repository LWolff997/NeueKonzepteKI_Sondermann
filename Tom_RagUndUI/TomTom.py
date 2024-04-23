from langchain.chains.combine_documents import create_stuff_documents_chain
import os
import streamlit as st
from dotenv import load_dotenv
import time
import pandas as pd
import re
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

# Retrieve the env variables
model = os.getenv('MODEL')
api_endpoint = os.getenv('API_ENDPOINT')
openai_api_base = api_endpoint + '/v1'
runpod_api_key = os.getenv('RUNPOD_API_KEY') if os.getenv('RUNPOD_API_KEY') is not None else "EMPTY"

# Initialize the OpenAI client
client = OpenAI(
    api_key=runpod_api_key,
    base_url=openai_api_base,
)

st.title("EducationAId")

def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() if page.extract_text() else ""
    return text

# Load and process PDF
pdf_path = "Biologie_extracted.pdf"
pdf_text = load_pdf(pdf_path)

if "vector" not in st.session_state:
    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    text_chunks = st.session_state.text_splitter.split_text(pdf_text)
    documents = [Document(page_content=chunk) for chunk in text_chunks if len(chunk) > 50]
    
    # Use HuggingFaceHubEmbeddings for embedding the text
    embed = HuggingFaceHubEmbeddings()
    st.session_state.vector = FAISS.from_documents(documents, embed)

retriever = st.session_state.vector.as_retriever()

# Create a prompt template to use with the local LLM
prompt_template = ChatPromptTemplate.from_template('''
    Du bist deutschsprachiger Biologie-Experte und Lehrer.
    Beantworte die Frage basierend auf dem folgenden Kontext.
    Halte dich immer besonders genau an den vorgegebenen Inhalt des Kontexts, also an die Originalquelle. Deine Hauptaufgabe ist es, Fragen über diesen Kontext hinweg zu beantworten und den Kontext besonders zugänglich zu machen.                    
    <Kontext>
    {context}
    </Kontext>

    Frage: {input}
''')

def get_llm_response(context, question):
    # Assuming `context` and `question` are the correct keys for your template variables
    formatted_prompt = prompt_template.format(context=context, input=question)
    messages = [
        {"role": "system", "content": formatted_prompt}
    ]
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten bei der Fragestellung: {str(e)}")
        return "Fehler: Antwort konnte nicht verarbeitet werden."

document_chain = create_stuff_documents_chain(
    llm=lambda args: get_llm_response(getattr(args, 'context', None), getattr(args, 'input', None)),
    prompt=prompt_template
)



retrieve_chain = create_retrieval_chain(retriever, document_chain)

user_prompt = st.text_input("Stelle eine Frage, die dir EducationAId beantworten soll:")
if user_prompt:
    start = time.process_time()
    response = retrieve_chain.invoke({"input": user_prompt, "context": pdf_text})
    st.write(response['answer'])

    with st.expander("Dokumentenabgleich:"):
        for doc in response['context']:
            st.write(doc.page_content)
            st.write("==============")