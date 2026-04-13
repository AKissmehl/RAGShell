"""
Configuration Module.

This module handles loading and managing configuration for the RAG system.
"""

from typing import Dict, Any, Optional

import yaml


class RAGConfig:
    """Configuration manager for RAG system."""
    
    DEFAULT_DATA_PATH = "data/wiki_dump/"

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.

        Args:
            config_path: Path to the configuration file. If None, uses default.
        """
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_default_config()

    def _get_default_config_path(self) -> str:
        """
        Get the default configuration file path.

        Returns:
            Path to the default configuration file.
        """
        return "config.yaml"

    def _load_default_config(self) -> Dict[str, Any]:
        """
        Load the default configuration.

        Returns:
            Default configuration dictionary.
        """
        return {
            "llm": {
                "provider": "llama_cpp",
                "model_path": "models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
                "context_window": 2048,
                "generation_params": {
                    'max_tokens': 256,
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'echo': False
                }
            },
            "rag": {
                "embedding_model": "all-MiniLM-L6-v2",
                "chunk_size": 512,
                "chunk_overlap": 50,
                "persist_directory": "data/vector_db",
                "data_path": self.DEFAULT_DATA_PATH
            },
            "download": {
                "repo_id": "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
                "filename": "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
                "local_dir": "models",
                "expected_path": "models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
                "repo_type": "model"
            }
        }

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.

        Returns:
            Configuration dictionary.

        Raises:
            FileNotFoundError: If configuration file does not exist.
            yaml.YAMLError: If configuration file is invalid.
        """
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            return self.config
        except FileNotFoundError:
            # Create default config file if it doesn't exist
            self.save_config(self.config)
            return self.config
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML in configuration file: {str(e)}")

    def save_config(self, config: Dict[str, Any]):
        """
        Save configuration to file.

        Args:
            config: Configuration dictionary to save.
        """
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    def get_llm_config(self) -> Dict[str, Any]:
        """
        Get LLM configuration.

        Returns:
            LLM configuration dictionary.
        """
        return self.config.get("llm", {})

    def get_rag_config(self) -> Dict[str, Any]:
        """
        Get RAG configuration.

        Returns:
            RAG configuration dictionary.
        """
        return self.config.get("rag", {})

    def get_download_config(self) -> Dict[str, Any]:
        """
        Get download configuration.

        Returns:
            Download configuration dictionary.
        """
        return self.config.get("download", {})

    def update_config(self, updates: Dict[str, Any]):
        """
        Update configuration.

        Args:
            updates: Dictionary of updates to apply.
        """
        self._deep_update(self.config, updates)

    def _deep_update(self, original: Dict[str, Any], updates: Dict[str, Any]):
        """
        Deep update a dictionary.

        Args:
            original: Original dictionary.
            updates: Updates to apply.
        """
        for key, value in updates.items():
            if isinstance(value, dict) and key in original and isinstance(original[key], dict):
                self._deep_update(original[key], value)
            else:
                original[key] = value

    def get_config_path(self) -> str:
        """
        Get the configuration file path.

        Returns:
            Path to the configuration file.
        """
        return self.config_path
