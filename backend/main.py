from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from PIL import Image
import pytesseract
from gtts import gTTS
from deep_translator import GoogleTranslator
import tempfile
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

PORT = int(os.getenv("PORT", 10000))

# Paths
BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_AUDIO_DIR = FRONTEND_DIR / "audio"
STATIC_AUDIO_DIR.mkdir(exist_ok=True)

# Tesseract paths (Linux / Railway)
tesseract_path = "/usr/bin/tesseract"
tessdata_dir_path = "/usr/share/tesseract-ocr/tessdata"

pytesseract.pytesseract.tesseract_cmd = tesseract_path

app = FastAPI()

# Serve static frontend
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Language map
LANG_CODE_MAP = {
    'eng': 'en',
    'spa': 'es',
    'fra': 'fr',
    'deu': 'de',
    'ita': 'it',
    'por': 'pt',
    'rus': 'ru',
    'jpn': 'ja',
    'chi_sim': 'zh-cn',
    'ara': 'ar',
    'hin': 'hi'
}

@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/ocr-tts/")
async def ocr_tts(
    file: UploadFile = File(...),
    source_lang: str = Form("eng"),
    target_lang: str = Form("en"),
    translate: str = Form("false")
):
    try:
        contents = await file.read()

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp.write(contents)
            temp_path = tmp.name

        img = Image.open(temp_path)
        text = pytesseract.image_to_string(img, lang=source_lang)

        if not text.strip():
            return JSONResponse({"error": "No text found!"}, status_code=400)

        # translation
        final_text = text.strip()
        translated_text = None

        if translate == "true":
            source_iso = LANG_CODE_MAP.get(source_lang, "en")
            translator = GoogleTrans
