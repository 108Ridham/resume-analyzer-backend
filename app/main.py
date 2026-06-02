import os
import shutil
import tempfile
import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.services.analyser import analyze_resume


logging.basicConfig(level=logging.INFO)             
logger = logging.getLogger(__name__)

app = FastAPI()

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Resume Analyzer API is running"}

@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    # ✅ Input validation
    if not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted")

    if len(job_description.strip()) < 50:
        raise HTTPException(status_code=400, detail="Job description too short (min 50 chars)")

    contents = await resume.read()
    if len(contents) > 5 * 1024 * 1024:             # 5MB limit
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    # ✅ Safe unique temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        result = analyze_resume(tmp_path, job_description)
        logger.info(f"Request processed | file={resume.filename}")
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")
    finally:
        os.remove(tmp_path)                         

    return result