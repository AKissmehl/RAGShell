"""
Vector Database Module.

This module provides integration with Chroma DB for storing and retrieving
document embeddings.
"""

from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings


class VectorDB:
    """Vector database interface using Chroma DB."""

    def __init__(self, collection_name: str = "documents", persist_directory: Optional[str] = None):
        """
        Initialize the vector database.

        Args:
            collection_name: Name of the collection to use.
            persist_directory: Directory to persist the database (optional).
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None

    def connect(self):
        """Connect to the vector database."""
        print("connect")
        if self.persist_directory:
            self.client = chromadb.PersistentClient(path=self.persist_directory)
        else:
            self.client = chromadb.Client(Settings(allow_reset=True))

        # Get or create collection
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """
        Add documents to the vector database.

        Args:
            documents: List of document texts.
            metadatas: List of metadata dictionaries.
            ids: List of document IDs.
        """
        if not self.collection:
            self.connect()

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Query the vector database.

        Args:
            query_text: The query text.
            top_k: Number of results to return.

        Returns:
            List of retrieved documents with metadata.
        """
        if not self.collection:
            self.connect()

        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k
        )

        # Format results
        retrieved_docs = []
        for i in range(len(results["ids"][0])):
            doc = {
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            }
            retrieved_docs.append(doc)

        return retrieved_docs

    def clear(self):
        """Clear the vector database."""
        if self.collection:
            # Get all documents and delete them
            results = self.collection.get()
            if results and results.get("ids"):
                self.collection.delete(ids=results["ids"])
