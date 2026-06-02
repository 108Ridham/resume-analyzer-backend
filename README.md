# 🤖 AI Resume Analyzer Backend (FastAPI)

The backend service for the AI Resume Analyzer, built with **FastAPI**. It handles parsing resume PDFs, checking ATS compliance, calculating semantic match scores, and calling the Groq API for personalized advice.

For detailed information on how the ATS Compatibility Score is calculated mathematically, please refer to the main [README.md](../README.md).

---

## ⚙️ How the Backend Works
*   **Advanced PDF Parsing (`pdf_parser.py`)**: Uses **PyMuPDF (`fitz`)** to extract raw text and embedded hyperlink annotations.
*   **Offline Semantic Match (`embeddings.py` & `matcher.py`)**: Vectorizes text based on technical and leadership keyword occurrences, computing cosine similarity using pure `numpy` math. Runs in microseconds with zero network calls and 0 MB extra memory overhead.
*   **Section Detection (`skills.py`)**: Scans for standard sections (Experience, Education, Skills, Projects) using synonyms.
*   **AI Coach (`llm.py`)**: Connects to the **Llama 3.1 8B Instant** model via the **Groq Cloud API** to generate targeted feedback and project ideas.

---

## 🚀 Local Run (Backend)

1. Activate your virtual environment:
   * **PowerShell**: `.venv\Scripts\Activate.ps1`
   * **Command Prompt**: `.venv\Scripts\activate.bat`
2. Run the development server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

---

## 🌐 Production Deployment

1. Connect your repository (`resume-analyzer-backend`) to **Render**.
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set **Environment Variables**:
   * `GROQ_API_KEY`: Your Groq Cloud API key.
   * `ALLOWED_ORIGINS`: Your Vercel frontend URL.
