# Base image
FROM python:3.13-slim

# Install Tesseract OCR and dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Set TESSDATA_PREFIX for tesseract
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/tessdata

# Set workdir
WORKDIR /app

# Copy backend and frontend
COPY backend/ ./backend
COPY backend/frontend ./frontend 
COPY frontend/ ./frontend

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Railway uses PORT env variable)
ENV PORT=8080
EXPOSE 8080

# Start the FastAPI app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
