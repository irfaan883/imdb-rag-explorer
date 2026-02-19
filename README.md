🎬 IMDB AI Assistant
Enterprise-Grade RAG Movie Intelligence Platform

An AI-powered movie intelligence system built using Retrieval-Augmented Generation (RAG) architecture.
This application enables structured, contextual, and reliable movie search using semantic embeddings and a local LLM.

Designed with clean architecture principles, modular services, and a Netflix-style UI.

🚀 Features
🧠 AI-Powered Movie Search

Semantic search using vector embeddings

Structured LLM responses

Context-aware retrieval (RAG pipeline)

Deterministic formatted output

🗂 Enterprise Architecture

Clean separation of concerns

Service-based modular design

Config-driven architecture

Cached vector store

Scalable folder structure

🎨 Professional UI

Netflix-inspired dark theme

Styled movie cards

Clean chat interface

Responsive layout

📊 Analytics Dashboard

Genre distribution

Rating distribution

Movies per year trends

Key dataset metrics

🏗 Architecture Overview
User Input
   ↓
Streamlit UI (app.py)
   ↓
RAG Service
   ├── Vector Store (ChromaDB)
   ├── Retriever (Top-K search)
   └── LLM Chain (Ollama + Prompt Template)
   ↓
Structured Movie Response
   ↓
Styled UI Rendering


This project follows a proper RAG architecture pattern:

Embeddings: mxbai-embed-large

Vector Store: Chroma

LLM: gemma3:1b (Ollama)

Framework: LangChain

UI: Streamlit

📁 Project Structure
imdb_ai_app/
│
├── app.py                 # Streamlit UI layer
├── config.py              # Central configuration
├── requirements.txt
│
├── data/
│   └── imdb_top_1000.csv
│
├── services/
│   ├── rag_service.py
│   ├── vector_store.py
│   └── llm_service.py
│
└── chroma_db/             # Persistent vector database

Layer Responsibilities
Layer	Responsibility
UI (app.py)	Rendering & interaction
rag_service	Orchestrates retrieval + generation
vector_store	Embeddings + persistence
llm_service	Prompt + LLM logic
config.py	Centralized configuration
🧠 RAG Implementation Details
1️⃣ Vector Store

Uses ChromaDB for persistence

Documents built from IMDB dataset

Embeddings generated using Ollama

2️⃣ Retrieval

Top-K semantic search

Context filtering before generation

3️⃣ Generation

Structured prompt template

Strict formatting enforcement

Context-bound answers only

💻 Tech Stack

Python

Streamlit

LangChain

Ollama

ChromaDB

Pandas

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/yourusername/imdb-ai-assistant.git
cd imdb-ai-assistant

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Install Ollama & Pull Models

Install Ollama from:

https://ollama.com/

Then pull required models:

ollama pull gemma3:1b
ollama pull mxbai-embed-large

4️⃣ Run the Application
streamlit run app.py

📊 Dataset

Source: IMDB Top 1000 Movies Dataset
Columns include:

Title

Release Year

Genre

Director

Stars

IMDB Rating

Overview

Votes

Gross Revenue

🔥 Key Engineering Highlights

No runtime re-embedding on every rerun

Persistent vector DB

Service-layer abstraction

Config-driven environment

Strict prompt formatting

Scalable design for multi-dataset expansion

Production-ready modular structure

🚀 Future Enhancements

🎞 TMDB Poster Integration

⚡ Streaming LLM Responses

🎯 Recommendation Engine

🧩 Multi-dataset Support

🐳 Dockerization

☁ Cloud Deployment

📈 Monitoring & Logging

🏆 Why This Project Matters

This project demonstrates:

Practical implementation of RAG

Clean AI system architecture

Modular design principles

Scalable ML system design

UI/UX integration with LLM systems

Production-ready code structure

It is not a prototype — it follows real-world AI system design patterns.

📄 License

MIT License
