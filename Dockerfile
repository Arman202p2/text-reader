FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    wget \
    ffmpeg \
    espeak \
    libespeak-ng1 \
    && rm -rf /var/lib/apt/lists/*

# Create tessdata directory
RUN mkdir -p /usr/share/tesseract-ocr/tessdata

# Download language files
RUN wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata -O /usr/share/tesseract-ocr/tessdata/eng.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/spa.traineddata -O /usr/share/tesseract-ocr/tessdata/spa.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/fra.traineddata -O /usr/share/tesseract-ocr/tessdata/fra.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/deu.traineddata -O /usr/share/tesseract-ocr/tessdata/deu.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/ita.traineddata -O /usr/share/tesseract-ocr/tessdata/ita.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/por.traineddata -O /usr/share/tesseract-ocr/tessdata/por.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/rus.traineddata -O /usr/share/tesseract-ocr/tessdata/rus.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/jpn.traineddata -O /usr/share/tesseract-ocr/tessdata/jpn.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata -O /usr/share/tesseract-ocr/tessdata/chi_sim.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/ara.traineddata -O /usr/share/tesseract-ocr/tessdata/ara.traineddata

WORKDIR /app

# Copy backend
COPY backend ./backend

# Install requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 10000
ENV PORT=10000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]
