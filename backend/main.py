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

load_dotenv()  # loads variables from .env file

tesseract_path = os.getenv("TESSERACT_PATH")
tessdata_dir_path = os.getenv("TESSERACT_LANG_DATA_PATH")

#pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your path
pytesseract.pytesseract.tesseract_cmd = tesseract_path

app = FastAPI()

# Allow frontend to access backend from browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],  # In production, specify your frontend domain instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

# Serve a default favicon (16x16 blank icon)
@app.get("/favicon.ico")
async def favicon():
    # A tiny transparent 16x16 favicon in bytes
    favicon_bytes = bytes.fromhex(
        "00000100010010100000010010000000000100000001000000000000000000000000000000"
    )
    return Response(content=favicon_bytes, media_type="image/x-icon")

@app.post("/ocr-tts/")
async def ocr_tts(file: UploadFile = File(...)):
    contents = await file.read()
    temp_file = "/tmp/temp.png"
    audio_file = "/tmp/voice.mp3"
    with open(temp_file, "wb") as f:
        f.write(contents)
    img = Image.open(temp_file)
    text = pytesseract.image_to_string(img)
    if not text.strip():
        return {"error": "No text found"}
    tts = gTTS(text=text, lang='en')
    tts.save(audio_file)
    return FileResponse(audio_file, media_type="audio/mpeg", filename="voice.mp3")
