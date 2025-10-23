# Base image
FROM python:3.13-slim

# Install Tesseract OCR and dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create custom tessdata directory
RUN mkdir -p /app/tessdata

# Download English trained data to custom location
RUN wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata -P /app/tessdata
# Set TESSDATA_PREFIX to custom location
ENV TESSDATA_PREFIX=/app/tessdata
# After tesseract installation, add:
RUN ls -la /app/tessdata/
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
