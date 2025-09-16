# Use official Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/download | bash

# Copy Python requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Pull the Qwen2.5 model in Ollama
RUN ollama pull qwen2.5:7b-instruct-q4_k_m

# Expose FastAPI port
EXPOSE 8000

# Start Ollama server in background, then start FastAPI
CMD ollama serve & \
    sleep 5 && \
    uvicorn main:app --host 0.0.0.0 --port 8000
