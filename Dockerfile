# Use official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libgomp1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama CLI manually (adjust for Linux)
RUN curl -fsSL https://ollama.com/download/linux -o /tmp/ollama.sh && \
    chmod +x /tmp/ollama.sh && \
    /tmp/ollama.sh && \
    rm /tmp/ollama.sh

# Copy Python requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Pull your model in Ollama
RUN ollama pull qwen2.5:7b-instruct-q4_k_m

# Expose ports for AI lint server
EXPOSE 8000 11434

# Start Ollama server and AI lint server together
CMD ollama serve --port 11434 & \
    sleep 5 && \
    uvicorn main:app --host 0.0.0.0 --port 8000
