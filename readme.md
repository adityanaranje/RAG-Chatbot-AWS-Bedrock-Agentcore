# Fitness RAG Bot with Amazon Bedrock AgentCore

A Retrieval-Augmented Generation (RAG) chatbot deployed on **Amazon
Bedrock AgentCore** that answers fitness-related questions using a
knowledge base and remembers conversation history across sessions.

The bot: - Retrieves fitness knowledge using **FAISS vector search** -
Uses **Groq LLM (Llama‑3.3‑70B)** for responses - Stores conversation
history using **AgentCore Memory** - Runs inside **Amazon Bedrock
AgentCore runtime**

------------------------------------------------------------------------

# Architecture

User Query ↓ AgentCore Runtime ↓ Memory Retrieval (AgentCoreMemoryStore)
↓ RAG Retrieval (FAISS Vector Store) ↓ LLM Generation (Groq /
Llama‑3.3‑70B) ↓ Store Conversation in AgentCore Memory

------------------------------------------------------------------------

# Features

-   Retrieval Augmented Generation (RAG)
-   Persistent memory across sessions
-   Amazon Bedrock AgentCore deployment
-   Groq LLM integration
-   FAISS vector database
-   LangChain based tools

------------------------------------------------------------------------

# Project Structure

    .
    ├── main.py
    ├── rag_tool.py
    ├── vector_store.py
    ├── documents/
    ├── pyproject.toml
    └── README.md

------------------------------------------------------------------------

# Prerequisites

You need:

-   AWS Account
-   AWS CLI configured
-   Python 3.12+
-   AgentCore CLI installed
-   Docker installed
-   Groq API Key

------------------------------------------------------------------------

# Environment Setup

Create environment variables:

Linux / Mac

    export GROQ_API_KEY=your_key

Windows

    set GROQ_API_KEY=your_key

------------------------------------------------------------------------

# Install Dependencies

    pip install -r requirements.txt

or if using `pyproject.toml`

    pip install .

------------------------------------------------------------------------

# Build Vector Store

Run the script that loads documents and builds FAISS index.

Example:

    python vector_store.py

This creates a FAISS index used for retrieval.

------------------------------------------------------------------------

# Run Locally

    python main.py

Or using uvicorn if FastAPI is used:

    uvicorn main:app --reload

------------------------------------------------------------------------

# Deploy to Amazon Bedrock AgentCore

### 1. Login to AWS

    aws configure

Set:

-   Access Key
-   Secret Key
-   Region

------------------------------------------------------------------------

### 2. Initialize AgentCore

Inside the project directory:

    agentcore init

This generates the **agentcore.yaml** configuration file.

------------------------------------------------------------------------

### 3. Configure Agent

Edit the configuration file:

    entrypoint: main:app
    language: python
    deployment_type: container
    platform: linux/arm64

Add your IAM execution role.

------------------------------------------------------------------------

### 4. Deploy Agent

    agentcore deploy

This step will:

-   Build a container
-   Push image to Amazon ECR
-   Create AgentCore runtime
-   Deploy the agent

------------------------------------------------------------------------

### 5. Set Environment Variables

Example:

    agentcore deploy --env GROQ_API_KEY=your_key

------------------------------------------------------------------------

# Invoke the Agent

Run:

    agentcore invoke "{'input':'How much water should I drink daily?'}"

Example response:

    {
     "answer": "The general recommendation is to drink 2–3 liters of water daily."
    }

------------------------------------------------------------------------

# Conversation Memory

The bot stores messages using:

    AgentCoreMemoryStore

Each session is stored using:

    (actor_id, thread_id)

This allows the bot to remember previous questions within the same
session.

Example:

    User: How much water should I drink daily?
    Assistant: 2‑3 liters

    User: What did I ask earlier?
    Assistant: You asked about daily water intake.

------------------------------------------------------------------------

# Useful Commands

Deploy

    agentcore deploy

Invoke

    agentcore invoke "{'input':'your question'}"

View logs

    aws logs tail /aws/bedrock-agentcore/runtimes/<runtime-name> --follow

------------------------------------------------------------------------

# Tech Stack

-   Amazon Bedrock AgentCore
-   LangChain
-   LangGraph Memory
-   FAISS
-   Groq LLM
-   Python

------------------------------------------------------------------------

# Future Improvements

-   Multi‑agent architecture
-   User preference memory
-   Streaming responses
-   API gateway integration
-   Web UI

------------------------------------------------------------------------

# Author

Aditya Naranje

AI / ML Engineer \| Generative AI \| LLM Applications
