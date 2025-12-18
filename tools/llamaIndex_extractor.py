# job_extraction_module.py
# A Python module to extract structured information from job advertisement texts
# using LlamaIndex with a local Ollama LLM (recommended: nuextract or nuextract:1.5),
# then chunk the original text, add extracted metadata, and store in ChromaDB.

import os
from typing import List, Optional

from pydantic import BaseModel, Field

from llama_index.core import VectorStoreIndex, Document, Settings, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb


class JobAdExtraction(BaseModel):
    """Structured schema for job advertisement extraction."""
    post_title: Optional[str] = Field(default=None, description="The job title or position name.")
    company_name: Optional[str] = Field(default=None, description="The name of the hiring company.")
    working_location: Optional[str] = Field(default=None, description="The work location (city, country, remote, etc.).")
    salary: Optional[str] = Field(default=None, description="Salary range or amount mentioned, including currency.")
    requirements: Optional[List[str]] = Field(default_factory=list, description="List of required skills, qualifications, experience, etc.")
    responsibilities: Optional[List[str]] = Field(default_factory=list, description="List of job duties and responsibilities.")


def setup_llm_and_embedder(
    ollama_model: str = "nuextract:1.5",  # Recommended: nuextract or nuextract:1.5 for best structured extraction
    embed_model_name: str = "BAAI/bge-small-en-v1.5",  # Lightweight, high-quality open-source embedding
    request_timeout: float = 120.0,
):
    """Setup global LLM and embedding model."""
    llm = Ollama(model=ollama_model, request_timeout=request_timeout)
    embed_model = HuggingFaceEmbedding(model_name=embed_model_name)

    Settings.llm = llm
    Settings.embed_model = embed_model


def extract_structured_data(text: str) -> JobAdExtraction:
    """Extract structured job info from raw text using the LLM with Pydantic output."""
    # Ollama's structured output (with recent models like nuextract) directly returns Pydantic objects
    extraction: JobAdExtraction = Settings.llm.structured_predict(
        output_cls=JobAdExtraction,
        prompt="Extract the following information from the job advertisement text below. "
               "If a field is not found, leave it empty/null. "
               "Return only the structured data.\n\n"
               f"Text:\n{text}",
    )
    return extraction


def process_and_index_job_ads(
    job_texts: List[str],
    collection_name: str = "job_ads",
    chroma_db_path: str = "./chroma_db",
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> VectorStoreIndex:
    """
    Process a list of job advertisement texts:
    - Extract structured metadata
    - Create Documents with metadata
    - Chunk them
    - Embed and store in ChromaDB
    Returns the VectorStoreIndex for querying.
    """
    # Setup Chroma client and collection
    chroma_client = chromadb.PersistentClient(path=chroma_db_path)
    chroma_collection = chroma_client.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    documents = []
    for i, raw_text in enumerate(job_texts):
        # Extract structured data
        extracted = extract_structured_data(raw_text)

        # Convert extracted to dict, filter None values for cleaner metadata
        metadata = {
            "post_title": extracted.post_title or "Unknown",
            "company_name": extracted.company_name or "Unknown",
            "working_location": extracted.working_location or "Unknown",
            "salary": extracted.salary or "Not specified",
            "requirements": " | ".join(extracted.requirements) if extracted.requirements else "None",
            "responsibilities": " | ".join(extracted.responsibilities) if extracted.responsibilities else "None",
            "source_id": f"job_{i}",
        }

        # Create Document with full raw text and extracted metadata
        doc = Document(text=raw_text, metadata=metadata)
        documents.append(doc)

    # Chunking
    node_parser = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    nodes = node_parser.get_nodes_from_documents(documents)

    # Build index and persist to ChromaDB
    index = VectorStoreIndex(nodes, storage_context=storage_context, show_progress=True)

    print(f"Indexed {len(nodes)} chunks from {len(job_texts)} job ads into ChromaDB collection '{collection_name}'.")
    return index


# Example usage
if __name__ == "__main__":
    # Prerequisites:
    # - Run `ollama pull nuextract:1.5` (or nuextract) for best results
    # - pip install llama-index llama-index-llms-ollama llama-index-embeddings-huggingface llama-index-vector-stores-chroma chromadb

    setup_llm_and_embedder(ollama_model="nuextract:1.5")

    sample_job_texts = [
        """Senior Python Developer at TechCorp
        Location: Hong Kong (Hybrid)
        Salary: HKD 50,000 - 70,000 per month
        Responsibilities:
        - Develop backend services
        - Maintain code quality
        Requirements:
        - 5+ years Python
        - Experience with Django
        - Good communication skills""",
        # Add more job ad texts here...
    ]

    index = process_and_index_job_ads(sample_job_texts)

    # Example query with metadata filtering
    query_engine = index.as_query_engine(similarity_top_k=5)
    response = query_engine.query("Find Python developer jobs in Hong Kong with salary over 50k")
    print(response)