# 🤖 AI Resume Analyzer Backend (FastAPI)

The backend service for the AI Resume Analyzer, built with **FastAPI**. It handles parsing resume PDFs, checking ATS compliance, calculating semantic match scores, and calling the Groq API for personalized advice.

---

## 📊 How the ATS Score is Calculated (Mathematical Formula)

The ATS Compatibility Score ($0 \text{ to } 100$) is calculated using a weighted composite formula:

$$\text{ATS Score} = (0.50 \times \text{Keyword Score}) + (0.30 \times \text{Formatting Score}) + (0.20 \times \text{Length Score})$$

### 1. Keyword Score (Weight: 50%)
Calculates the coverage of technical and leadership keywords present in your resume relative to the job description:
$$\text{Keyword Score} = \left( \frac{\text{Unique Whitelisted JD Keywords Found in Resume}}{\text{Total Unique Whitelisted JD Keywords}} \right) \times 100$$
*   **Whitelisting**: Evaluated against a curated, localized vocabulary (`TECHNICAL_AND_LEADERSHIP_KEYWORDS`) to filter out city names, filler words, and recruiter jargon, ensuring only relevant tech skills and leadership words are graded.

### 2. Formatting Score (Weight: 30%)
Calculates compliance with standard ATS-friendly formatting guidelines based on 6 heuristic checks:
$$\text{Formatting Score} = \left( \frac{\text{Passed Checks}}{6} \right) \times 100$$
The checks evaluate:
*   **Bullet points**: Checks if lists are structured with standard bullet markers (e.g., `•`, `-`).
*   **Email address**: Detects if contact email is present.
*   **Phone number**: Checks for standard contact phone numbers.
*   **Excessive ALL-CAPS**: Flags if too many non-acronym words are in all-caps.
*   **Standard characters**: Detects non-ASCII or fancy characters that confuse ATS parsers.
*   **Profile link**: Scans for GitHub, LinkedIn, or personal portfolio URLs.

### 3. Length Score (Weight: 20%)
ATS algorithms prefer detailed but concise resumes. The score is assigned based on the total word count of the PDF:
*   **Ideal Length** ($300 - 800$ words): **100** points
*   **Slightly Long** ($801 - 1200$ words): **70** points
*   **Too Short** ($< 300$ words): **40** points
*   **Too Long** ($> 1200$ words): **30** points

---

## 🛠️ Key Features

*   **Offline Semantic Match**: Constructs local, whitelisted term-frequency vectors and computes cosine similarity using pure `numpy` math. Runs in under **1 millisecond** with **0 MB** memory overhead (fully offline).
*   **ATS Checklist**: Live checklist of formatting standards to verify that your PDF parser will read the document successfully.
*   **Actionable AI Advice**: Leverages **Llama 3.1 8B Instant** (via Groq Cloud API) to generate resume improvement sections.

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
