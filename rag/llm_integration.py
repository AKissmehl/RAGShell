"""
LLM Integration Module.

This module provides integration with various LLM providers including:
- Llama.cpp (default)
- GPT4All (alternative)
- Mock LLM (for testing)
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import os


class BaseLLM(ABC):
    """Abstract base class for LLM integrations."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text from the LLM.

        Args:
            prompt: The input prompt.
            **kwargs: Additional generation parameters.

        Returns:
            Generated text.
        """
        pass


class MockLLM(BaseLLM):
    """Mock LLM for testing without a real LLM."""

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a mock response.

        Args:
            prompt: The input prompt.
            **kwargs: Additional generation parameters.

        Returns:
            Mock generated text.
        """
        return f"You forgot to set up the ChromaDB. Check the settings!"


class LlamaCppLLM(BaseLLM):
    """LLM integration using Llama.cpp."""

    def __init__(self, model_path: str, context_window: int = 2048):
        """
        Initialize Llama.cpp LLM.

        Args:
            model_path: Path to the GGUF model file.
            context_window: Context window size.
        """
        self.model_path = model_path
        self.context_window = context_window
        self.llama = None
        
        try:
            from llama_cpp import Llama
            self.llama = Llama(
                model_path=model_path,
                n_ctx=context_window
            )
        except ImportError:
            raise ImportError("llama-cpp-python is not installed. Please install it with: pip install llama-cpp-python")
        except Exception as e:
            raise RuntimeError(f"Failed to load Llama.cpp model: {str(e)}")

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Llama.cpp.

        Args:
            prompt: The input prompt.
            **kwargs: Additional generation parameters.

        Returns:
            Generated text.
        """
        if not self.llama:
            raise RuntimeError("Llama.cpp model is not loaded")

        # Set default generation parameters
        params = {
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "echo": False,
            **kwargs
        }

        try:
            result = self.llama(prompt, **params)
            return result["choices"][0]["text"]
        except Exception as e:
            return f"[Error] Failed to generate response: {str(e)}"


class GPT4AllLLM(BaseLLM):
    """LLM integration using GPT4All."""

    def __init__(self, model_path: str, context_window: int = 2048):
        """
        Initialize GPT4All LLM.

        Args:
            model_path: Path to the GPT4All model file.
            context_window: Context window size.
        """
        self.model_path = model_path
        self.context_window = context_window
        self.gpt4all = None
        
        try:
            from gpt4all import GPT4All
            self.gpt4all = GPT4All(
                model_name=model_path,
                model_path=model_path
            )
        except ImportError:
            raise ImportError("gpt4all is not installed. Please install it with: pip install gpt4all")
        except Exception as e:
            raise RuntimeError(f"Failed to load GPT4All model: {str(e)}")

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using GPT4All.

        Args:
            prompt: The input prompt.
            **kwargs: Additional generation parameters.

        Returns:
            Generated text.
        """
        if not self.gpt4all:
            raise RuntimeError("GPT4All model is not loaded")

        try:
            # GPT4All uses different parameter names
            params = {
                "max_tokens": kwargs.get("max_tokens", 512),
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.9),
            }

            result = self.gpt4all.generate(prompt, **params)
            return result
        except Exception as e:
            return f"[Error] Failed to generate response: {str(e)}"


class LLMIntegration:
    """Factory class for LLM integrations."""

    @staticmethod
    def create_llm(provider: str, model_path: str, context_window: int = 2048) -> BaseLLM:
        """
        Create an LLM instance based on the provider.

        Args:
            provider: LLM provider ('mock', 'llama_cpp', or 'gpt4all').
            model_path: Path to the model file.
            context_window: Context window size.

        Returns:
            BaseLLM instance.
        """
        provider = provider.lower()

        if provider == "mock":
            return MockLLM()
        elif provider == "llama_cpp":
            return LlamaCppLLM(model_path, context_window)
        elif provider == "gpt4all":
            return GPT4AllLLM(model_path, context_window)
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")
