# Local RAG Q&A System

## Overview

A locally hosted Retrieval-Augmented Generation (RAG)
question-answering system using PostgreSQL/pgvector
for vector similarity search and Ollama for local LLM
inference.

## Architecture

Documents
    ↓
Chunking
    ↓
nomic-embed-text
    ↓
Generate Embeddings for Chunk
    ↓
PostgreSQL + pgvector - Store Embeddings
    ↓
Raise a Query
    ↓

Top-K similarity retrieval
    ↓
Retrieved context
    ↓
Llama 3.2
    ↓
Answer

## Technologies

- Python
- Streamlit
- PostgreSQL
- pgvector
- Ollama
- llama 3.2 / qwen3.5:4b
- nomic-embed-text

## Features

- Document chunking
- Local embedding generation
- Vector storage
- Semantic similarity search
- Top-K retrieval
- Context-grounded generation
- Local LLM inference
- Interactive Streamlit interface

## Setup

1. Install PostgreSQL/pgvector
2. Install Ollama
3. Pull required models
4. Configure `.env`
5. Install Python dependencies
6. Run database schema
7. Run ingestion
8. Start Streamlit

## Running

streamlit run app.py