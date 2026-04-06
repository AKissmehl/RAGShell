"""
RAG Pipeline Module.

This module implements the core RAG (Retrieval-Augmented Generation) pipeline,
including document retrieval and answer generation.
"""

from typing import List, Dict, Any
from .vector_db import VectorDB
from .llm_integration import LLMIntegration


class RAGPipeline:
    """Core RAG pipeline for retrieval and generation."""

    def __init__(self, vector_db: VectorDB, llm_integration: LLMIntegration):
        """
        Initialize the RAG pipeline.

        Args:
            vector_db: VectorDB instance for document retrieval.
            llm_integration: LLMIntegration instance for answer generation.
        """
        self.vector_db = vector_db
        self.llm_integration = llm_integration

    def retrieve_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents from the vector database.

        Args:
            query: The user's query.
            top_k: Number of documents to retrieve.

        Returns:
            List of retrieved documents with metadata.
        """
        return self.vector_db.query(query, top_k=top_k)

    def generate_answer(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        """
        Generate an answer using the LLM with retrieved documents as context.

        Args:
            query: The user's query.
            retrieved_docs: List of retrieved documents.

        Returns:
            Generated answer string.
        """
        # Format the context from retrieved documents
        context = "\n\n".join([doc["content"] for doc in retrieved_docs])

        # Create the prompt with context
        prompt = f"""
        Context:
        {context}

        Question: {query}

        Answer:
        """

        # Generate answer using LLM
        return self.llm_integration.generate(prompt)

    def answer_question(self, query: str, top_k: int = 3) -> str:
        """
        Full RAG pipeline: retrieve documents and generate answer.

        Args:
            query: The user's query.
            top_k: Number of documents to retrieve.

        Returns:
            Generated answer string.
        """
        # Retrieve relevant documents
        retrieved_docs = self.retrieve_documents(query, top_k=top_k)

        # Generate answer using retrieved documents
        return self.generate_answer(query, retrieved_docs)
