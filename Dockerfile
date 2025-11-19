# Base image
FROM python:3.13-slim

# Prevent Python from writing pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Tesseract OCR and dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    wget \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Create tessdata directory if it doesn't exist
RUN mkdir -p /usr/share/tesseract-ocr/tessdata

# Download language files
RUN wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata -O /usr/share/tesseract-ocr/tessdata/eng.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/hin.traineddata -O /usr/share/tesseract-ocr/tessdata/hin.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/spa.traineddata -O /usr/share/tesseract-ocr/tessdata/spa.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/fra.traineddata -O /usr/share/tesseract-ocr/tessdata/fra.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/deu.traineddata -O /usr/share/tesseract-ocr/tessdata/deu.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/ita.traineddata -O /usr/share/tesseract-ocr/tessdata/ita.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/por.traineddata -O /usr/share/tesseract-ocr/tessdata/por.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/rus.traineddata -O /usr/share/tesseract-ocr/tessdata/rus.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/jpn.traineddata -O /usr/share/tesseract-ocr/tessdata/jpn.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata -O /usr/share/tesseract-ocr/tessdata/chi_sim.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/asm.traineddata -O /usr/share/tesseract-ocr/tessdata/asm.traineddata &&\
    wget https://github.com/tesseract-ocr/tessdata/raw/main/ben.traineddata -O /usr/share/tesseract-ocr/tessdata/ben.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/guj.traineddata -O /usr/share/tesseract-ocr/tessdata/guj.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/kan.traineddata -O /usr/share/tesseract-ocr/tessdata/kan.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/mal.traineddata -O /usr/share/tesseract-ocr/tessdata/mal.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/mar.traineddata -O /usr/share/tesseract-ocr/tessdata/mar.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/mni.traineddata -O /usr/share/tesseract-ocr/tessdata/mni.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/ori.traineddata -O /usr/share/tesseract-ocr/tessdata/ori.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/pan.traineddata -O /usr/share/tesseract-ocr/tessdata/pan.traineddata &&\
    wget https://github.com/tesseract-ocr/tessdata/raw/main/san.traineddata -O /usr/share/tesseract-ocr/tessdata/san.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/snd.traineddata -O /usr/share/tesseract-ocr/tessdata/snd.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/tam.traineddata -O /usr/share/tesseract-ocr/tessdata/tam.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/tel.traineddata -O /usr/share/tesseract-ocr/tessdata/tel.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/urd.traineddata -O /usr/share/tesseract-ocr/tessdata/urd.traineddata

# Verify installation
RUN ls -la /usr/share/tesseract-ocr/tessdata/ && \
    tesseract --list-langs
# Set workdir
WORKDIR /app

# Copy backend and frontend
COPY backend/ ./backend
COPY backend/frontend ./frontend 

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Railway uses PORT env variable)
ENV PORT=8080
EXPOSE 8080

# Start the FastAPI app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
