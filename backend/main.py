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

# Base paths
BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR / "frontend"
AUDIO_DIR = FRONTEND_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)  # Ensure audio folder exists

# Tesseract paths (Linux/Railway)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
TESSDATA_PATH = "/usr/share/tesseract-ocr/tessdata"

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

# FastAPI app
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static route for frontend
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/health")
def health_check():
    """Health check endpoint for Railway."""
    return {
        "status": "healthy",
        "tesseract_path": pytesseract.pytesseract.tesseract_cmd,
        "tessdata_path": TESSDATA_PATH,
        "frontend_dir": str(FRONTEND_DIR),
        "audio_dir": str(AUDIO_DIR)
    }

@app.get("/", response_class=HTMLResponse)
def home():
    """Serve the frontend."""
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        return HTMLResponse(
            content=f"<h1>Frontend not found</h1><p>Looking for: {index_path}</p><p>BASE_DIR: {BASE_DIR}</p>",
            status_code=404
        )
    return FileResponse(index_path)

@app.post("/ocr-tts/")
async def ocr_tts(
    file: UploadFile = File(...),
    source_lang: str = Form("eng"),
    target_lang: str = Form("en"),
    translate: str = Form("false")
):
    temp_img_path = None
    try:
        # Read uploaded image
        contents = await file.read()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp.write(contents)
            temp_img_path = tmp.name
        
        # OCR
        img = Image.open(temp_img_path)
        text = pytesseract.image_to_string(
            img,
            lang=source_lang,
            config=f'--tessdata-dir "{TESSDATA_PATH}"'
        )
        extracted_text = text.strip()
        
        if not extracted_text:
            return JSONResponse({"error": "No text detected in image!"}, status_code=400)
        
        final_text = extracted_text
        translated_text = None
        
        # Translation (optional)
        if translate == "true":
            try:
                source_iso = LANG_CODE_MAP.get(source_lang, "en")
                translator = GoogleTranslator(source=source_iso, target=target_lang)
                translated_text = translator.translate(final_text)
                final_text = translated_text
            except Exception as e:
                print("Translation error:", e)
                return JSONResponse({"error": f"Translation failed: {str(e)}"}, status_code=500)
        
        # Generate TTS
        audio_filename = f"audio_{os.path.basename(temp_img_path)}.mp3"
        audio_path = AUDIO_DIR / audio_filename
        tts = gTTS(final_text, lang=target_lang)
        tts.save(audio_path)
        
        # Response
        response_data = {
            "extracted_text": extracted_text,
            "audio_url": f"/static/audio/{audio_filename}",
        }
        if translated_text:
            response_data["translated_text"] = translated_text
        
        return JSONResponse(response_data)
        
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)
    
    finally:
        # Cleanup temporary file
        if temp_img_path and os.path.exists(temp_img_path):
            try:
                os.unlink(temp_img_path)
            except:
                pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
