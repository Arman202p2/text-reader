from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
from gtts import gTTS
import os
from dotenv import load_dotenv
from fastapi.responses import Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import tempfile
from pathlib import Path

load_dotenv()  # loads variables from .env file

tesseract_path = os.getenv("TESSERACT_PATH", "/usr/bin/tesseract")
tessdata_dir_path = os.getenv("TESSERACT_LANG_DATA_PATH", "/usr/share/tesseract-ocr/4.00/tessdata")

#pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your path
pytesseract.pytesseract.tesseract_cmd = tesseract_path
custom_config = f'--tessdata-dir "{tessdata_dir_path}"' if tessdata_dir_path else ""

app = FastAPI()

app.mount("/static", StaticFiles(directory=Path(__file__).parent / "frontend", html=True), name="frontend")
# Allow frontend to access backend from browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL") or "*"],  # In production, specify your frontend domain instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Path to the frontend index.html
frontend_index = Path(__file__).parent / "frontend" / "index.html"


@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse(frontend_index)

# Serve a default favicon (16x16 blank icon)
@app.get("/favicon.ico")
async def favicon():
    # A tiny transparent 16x16 favicon in bytes
    favicon_bytes = bytes.fromhex(
        "00000100010010100000010010000000000100000001000000000000000000000000000000"
    )
    return Response(content=favicon_bytes, media_type="image/x-icon")

@app.post("/ocr-tts/")
@app.post("/ocr-tts/")
async def ocr_tts(file: UploadFile = File(...)):
    try:
        # Debug: Print paths
        print("Tesseract path:", pytesseract.pytesseract.tesseract_cmd)
        print("Tessdata dir path:", tessdata_dir_path)
        print("Uploaded file:", file.filename)

        # Read uploaded image
        contents = await file.read()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
            tmp_img.write(contents)
            temp_file = tmp_img.name
        print("Temporary image path:", temp_file)

        # Open image and run OCR
        img = Image.open(temp_file)
        text = pytesseract.image_to_string(img, config=f'--tessdata-dir "{tessdata_dir_path}"')
        print("OCR extracted text:", repr(text))  # Debug: show exactly what was extracted

        if not text.strip():
            return {"error": "No text found. Check Tesseract binary and tessdata path!"}

        # Generate audio
        audio_file = temp_file.replace(".png", ".mp3")
        tts = gTTS(text=text, lang='en')
        tts.save(audio_file)
        print("Audio file created:", audio_file)

        return FileResponse(audio_file, media_type="audio/mpeg", filename="voice.mp3")

    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}
