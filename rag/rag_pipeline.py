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

    def __init__(self, vector_db: VectorDB, llm_integration: LLMIntegration, system_prompt: str = ""):
        """
        Initialize the RAG pipeline.

        Args:
            vector_db: VectorDB instance for document retrieval.
            llm_integration: LLMIntegration instance for answer generation.
            system_prompt: System prompt to guide LLM behavior.
        """
        self.vector_db = vector_db
        self.llm_integration = llm_integration
        self.system_prompt = system_prompt

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

        # Create the prompt with system prompt as instruction, not pattern
        system_instruction = self.system_prompt.split('Example Questions:')[0].strip() if 'Example Questions:' in self.system_prompt else self.system_prompt
        
        prompt = f"""
        {system_instruction}

        Context:
        {context}

        Question: {query}

        Answer:
        """

        # Generate answer using LLM
        full_response = self.llm_integration.generate(prompt)
        
        # Post-process to remove additional Q&A patterns that the LLM sometimes generates
        # Look for the first complete answer and return only that
        lines = full_response.split('\n')
        clean_answer = []
        
        for line in lines:
            # Stop if we detect the start of another Q&A cycle
            if line.strip().startswith('Question:') or line.strip().startswith('Answer:'):
                break
            clean_answer.append(line)
        
        # Join and clean up the answer
        result = '\n'.join(clean_answer).strip()
        
        # If we got an empty result (unlikely), return the original
        return result if result else full_response

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
