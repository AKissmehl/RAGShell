# RAGShell

A simple RAG (Retrieval-Augmented Generation) system for educational purposes with local LLM support. It is man to be 
used in a Lab to undersand how RAG work and how we can uses it for diffrent applicaiton. Primaaralyy is will be fosuced 
on the use as a Pegaical agenget that can provide informaiton about the Artemis program. 

## Quick Start

### todo add a description here. 

## Features

- **Local LLM**: TinyLlama 1.1B (700MB, runs on 4GB RAM)
- **Document Processing**: PDF, TXT, MD support
- **Vector Database**: Chroma DB for efficient retrieval
- **RAG Pipeline**: Complete retrieval-augmented generation
- **CLI Interface**: Easy to use menu system

## Configuration

Edit `config.yaml` to customize:
- LLM provider (mock, llama_cpp, gpt4all)
- Model paths and parameters
- Document chunking settings
- Vector database persistence
- System prompt
- 

## Requirements

- **Minimum**: 4GB RAM (for TinyLlama)
- **Recommended**: 8GB RAM (for larger models)
- **Disk Space**: ~1GB for TinyLlama model

## Alternative Models

For different hardware requirements:
- **Phi-2 (2.7B)**: Better performance, needs 6GB RAM
- **Mistral-7B**: More capable, needs 8GB RAM
- **Llama-2-7B**: Most capable, needs 8GB RAM

See `TINYLLAMA_SETUP.md` for detailed setup instructions.
