"""
RAG (Retrieval-Augmented Generation) module for RAGShell.

This module provides the core functionality for document processing,
vector storage, retrieval, and generation using LLMs.
"""

from .vector_db import VectorDB
from .document_processor import DocumentProcessor
from .llm_integration import LLMIntegration, BaseLLM
from .rag_pipeline import RAGPipeline
from .config import RAGConfig
