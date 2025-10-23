# 1️⃣ Base image
FROM python:3.13-slim

# 2️⃣ Install system packages (Tesseract + dependencies)
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev tesseract-ocr-eng && \
    rm -rf /var/lib/apt/lists/*

# 3️⃣ Set working directory
WORKDIR /app

# 4️⃣ Copy and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copy backend and frontend code
COPY backend/ ./backend
COPY frontend/ ./frontend

# 6️⃣ Expose Render port (Render injects PORT=10000 internally)
EXPOSE 8080

# 7️⃣ Run FastAPI app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
