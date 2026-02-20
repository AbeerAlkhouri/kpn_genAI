from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import logging
from typing import List
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

def load_documents_from_folder(folder_path: str) -> List[Document]:
    documents = []
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
            elif filename.endswith(".docx"):
                loader = Docx2txtLoader(file_path)
                documents.extend(loader.load())
            elif filename.endswith(".txt"):
                loader = TextLoader(file_path)
                documents.extend(loader.load())
        except Exception as e:
            logger.warning(f"Failed to load {filename}: {str(e)}")
            continue

    return documents

def split_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 100) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(documents)
