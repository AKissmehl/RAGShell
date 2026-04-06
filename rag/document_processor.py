"""
Document Processor Module.

This module handles document loading, splitting, and embedding for the RAG pipeline.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib

from sympy.codegen import Print
from torchgen.api.lazy import process_ir_type


class DocumentProcessor:
    """Document processor for loading, splitting, and embedding documents."""

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        """
        Initialize the document processor.

        Args:
            chunk_size: Size of document chunks in characters.
            chunk_overlap: Overlap between chunks in characters.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_document(self, file_path: str) -> str:
        """
        Load a document from file.

        Args:
            file_path: Path to the document file.

        Returns:
            Document content as string.

        Raises:
            ValueError: If file format is not supported.
        """
        file_ext = Path(file_path).suffix.lower()

        if file_ext == ".txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif file_ext == ".md":
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif file_ext == ".pdf":
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
            except ImportError:
                raise ImportError("PyPDF2 is not installed. Please install it with: pip install PyPDF2")
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")

    def split_document(self, document: str) -> List[str]:
        """
        Split a document into chunks.

        Args:
            document: Document content as string.

        Returns:
            List of document chunks.
        """
        chunks = []
        start = 0
        doc_length = len(document)
        
        while start < doc_length:
            end = min(start + self.chunk_size, doc_length)
            chunk = document[start:end]
            chunks.append(chunk)
            
            # Calculate next start position with overlap
            # Ensure we always move forward, even if overlap is large
            next_start = end - self.chunk_overlap
            
            # If overlap would take us backwards or keep us in place, move forward by 1
            if next_start <= start or next_start <= 0:
                start = end  # Move to end of current chunk
            else:
                start = next_start  # Use overlapped position
        
        return chunks

    def generate_document_id(self, file_path: str, chunk_index: int) -> str:
        """
        Generate a unique ID for a document chunk.

        Args:
            file_path: Path to the document file.
            chunk_index: Index of the chunk.

        Returns:
            Unique document ID.
        """
        # Create a hash of the file path and chunk index
        unique_string = f"{file_path}:{chunk_index}"
        return hashlib.md5(unique_string.encode()).hexdigest()

    def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Process a document: load, split, and prepare for embedding.

        Args:
            file_path: Path to the document file.

        Returns:
            Dictionary containing:
            - documents: List of document chunks
            - metadatas: List of metadata dictionaries
            - ids: List of document IDs
        """
        # Load document
        print("load documents")
        document_content = self.load_document(file_path)

        # Split document
        print("create chunks")
        chunks = self.split_document(document_content)
        print("create metadatas")
        metadatas = []
        ids = []
        # Generate metadata and IDs
        documents = []
        metadatas = []
        ids = []
        print("Chunck loop ")
        for i, chunk in enumerate(chunks):
            doc_id = self.generate_document_id(file_path, i)
            
            documents.append(chunk)
            metadatas.append({
                "source": file_path,
                "chunk_index": i,
                "total_chunks": len(chunks)
            })
            ids.append(doc_id)

        return {
            "documents": documents,
            "metadatas": metadatas,
            "ids": ids
        }

    def process_multiple_documents(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Process multiple documents.

        Args:
            file_paths: List of file paths.

        Returns:
            Dictionary containing:
            - documents: List of all document chunks
            - metadatas: List of all metadata dictionaries
            - ids: List of all document IDs
        """
        print("load documents in multupel loop")
        all_documents = []
        all_metadatas = []
        all_ids = []

        for file_path in file_paths:
            result = self.process_document(file_path)
            all_documents.extend(result["documents"])
            all_metadatas.extend(result["metadatas"])
            all_ids.extend(result["ids"])

        return {
            "documents": all_documents,
            "metadatas": all_metadatas,
            "ids": all_ids
        }
