# OCR to Speech

This project is a multi-faceted application that performs Optical Character Recognition (OCR) on images and converts the extracted text to speech. It consists of three main components:

*   **Backend**: A FastAPI application that provides an API for OCR and text-to-speech conversion.
*   **Desktop**: A PyQt5 desktop application that allows users to capture images from their camera, perform OCR, and listen to the extracted text.
*   **Frontend**: A simple web interface that allows users to upload an image and listen to the extracted text.

## Backend

The backend is a FastAPI application that provides a single endpoint, `/ocr-tts/`, for performing OCR and text-to-speech conversion.

### Setup

1.  Install the required Python packages:
    ```bash
    pip install -r backend/requirements.txt
    ```
2.  Install Tesseract OCR. For detailed instructions, see the official Tesseract documentation: [https://tesseract-ocr.github.io/tessdoc/Installation.html](https://tesseract-ocr.github.io/tessdoc/Installation.html)
3.  Create a `.env` file in the `backend` directory with the following variables:
    ```
    TESSERACT_PATH=<path_to_tesseract_executable>
    TESSERACT_LANG_DATA_PATH=<path_to_tessdata_directory>
    ```

### Usage

1.  Start the backend server:
    ```bash
    uvicorn backend.main:app --host 0.0.0.0 --port 10000
    ```
2.  The API will be available at `http://localhost:10000`.

## Desktop

The desktop application is a PyQt5 application that allows users to capture images from their camera, perform OCR, and listen to the extracted text.

### Setup

1.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
2.  Install Tesseract OCR. For detailed instructions, see the official Tesseract documentation: [https://tesseract-ocr.github.io/tessdoc/Installation.html](https://tesseract-ocr.github.io/tessdoc/Installation.html)
3.  Create a `.env` file in the `desktop` directory with the following variables:
    ```
    TESSERACT_PATH=<path_to_tesseract_executable>
    TESSERACT_LANG_DATA_PATH=<path_to_tessdata_directory>
    ```

### Usage

1.  Run the desktop application:
    ```bash
    python desktop/ocr_text_to_speech.py
    ```
2.  Click the "Start" button to start the camera.
3.  Click the "Snap Shot" button to take a picture, perform OCR, and listen to the extracted text.

## Frontend

The frontend is a simple web interface that allows users to upload an image and listen to the extracted text.

### Usage

1.  Make sure the backend server is running.
2.  Open the `frontend/index.html` file in your web browser.
3.  Select an image file and click the "Convert" button.
