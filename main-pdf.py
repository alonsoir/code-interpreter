import os

from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI


def calcular_valores_segmentacion(tamano_archivo, complejidad_archivo):
    # Calcular chunk_size basado en el tamaño del archivo
    chunk_size = (
        tamano_archivo // 25
    )  # Dividir el tamaño del archivo por 10 (ajustable según necesidades)

    if complejidad_archivo == "alta":
        chunk_overlap = (
            chunk_size // 35
        )  # Usar un solapamiento del 10% del chunk_size para archivos complejos
    elif complejidad_archivo == "baja":
        chunk_overlap = (
            chunk_size // 25
        )  # Usar un solapamiento del 20% del chunk_size para archivos menos complejos

    return chunk_size, chunk_overlap


def main(query, filename, chunk_size, chunk_overlap):
    print("Hello main-pdf!")
    # read in your pdf file
    pdf_reader = PdfReader(filename)
    # read data from the file and put them into a variable called text
    text = readDataFromFile(pdf_reader)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    texts = text_splitter.split_text(text)
    # Download embeddings from OpenAI
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(texts, embeddings)
    chain = load_qa_chain(OpenAI(), chain_type="stuff")
    docs = docsearch.similarity_search(query)
    # Filtrar los documentos relevantes para la pregunta
    filtered_docs = filter_relevant_docs(docs, query)
    print(f"query is {query}.")
    if filtered_docs:
        res = chain.run(input_documents=filtered_docs, question=query)
        print(res)
    else:
        print("No relevant documents found.")


def readDataFromFile(pdf_reader):
    text = ""
    for i, page in enumerate(pdf_reader.pages):
        text += page.extract_text()
    return text


def filter_relevant_docs(docs, query):
    """Filtra los documentos relevantes para la pregunta"""
    query_parts = query.strip().split()
    for doc in docs:
        doc_parts = doc.page_content.strip().split()
        if any(part in doc_parts for part in query_parts):
            yield doc


def obtener_tamano_archivo(ruta_archivo):
    tamaño_bytes = os.path.getsize(ruta_archivo)
    return tamaño_bytes


if __name__ == "__main__":
    load_dotenv()
    query = "Is there any Github profile url in the document?"
    filename = "mycv.pdf"
    # alta o baja
    complejidad = "baja"
    tamanyo_bytes = obtener_tamano_archivo(filename)
    chunk_size, chunk_overlap = calcular_valores_segmentacion(
        tamanyo_bytes, complejidad
    )
    print(
        f"file is {filename} complexity is {complejidad} length file is {tamanyo_bytes} chunk_size is {chunk_size} chunk_overlap is {chunk_overlap}."
    )
    main(query, filename, chunk_size, chunk_overlap)
