# Use official Python 3.10 image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy your app code
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install fastapi uvicorn requests

# Expose port 8000
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
