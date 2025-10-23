from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
from gtts import gTTS
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env file

tesseract_path = os.getenv("TESSERACT_PATH")
tessdata_dir_path = os.getenv("TESSERACT_LANG_DATA_PATH")

#pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your path
pytesseract.pytesseract.tesseract_cmd = tesseract_path

app = FastAPI()

# Allow frontend to access backend from browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ocr-tts/")
async def ocr_tts(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp.png", "wb") as f:
        f.write(contents)
    img = Image.open("temp.png")
    text = pytesseract.image_to_string(img)
    if not text.strip():
        return {"error": "No text found"}
    tts = gTTS(text=text, lang='en')
    tts.save("voice.mp3")
    return FileResponse("voice.mp3", media_type="audio/mpeg", filename="voice.mp3")
