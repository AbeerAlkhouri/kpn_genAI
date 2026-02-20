from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from core.config import settings
from utils.loaders import load_documents_from_folder, split_documents
import logging

logger = logging.getLogger(__name__)

class IngestionService:
    def __init__(self):
        self.embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            openai_api_key=settings.AZURE_OPENAI_KEY,
            azure_deployment=settings.AZURE_EMBEDDING_DEPLOYMENT,
            api_version=settings.AZURE_OPENAI_API_VERSION,
        )
        self.vector_store = None

    def initialize_vector_store(self):
        try:
            folder_path = settings.SHARED_FOLDER
            logger.info(f"RAG Initialization - Loading documents from {folder_path}...")

            raw_docs = load_documents_from_folder(folder_path)
            if not raw_docs:
                logger.info(f"RAG Initialization - No documents found in {folder_path}.")
                return

            chunks = split_documents(raw_docs)
            logger.info(f"RAG Initialization - Created {len(chunks)} chunks from {len(raw_docs)} documents.")

            self.vector_store = FAISS.from_documents(chunks, self.embeddings)
            logger.info("RAG Initialization - Vector store successfully initialized in memory.")

        except Exception as e:
            logger.error(f"Failed to initialize vector store: {str(e)}")

    def similarity_search(self, query: str, k: int = 3) -> str:
        if not self.vector_store:
            return "Knowledge base is currently empty or not initialized."

        try:
            docs = self.vector_store.similarity_search(query, k=k)
            context = "\n\n".join([doc.page_content for doc in docs])
            return context
        except Exception as e:
            return f"Error searching knowledge base: {str(e)}"


ingestion_service = IngestionService()


