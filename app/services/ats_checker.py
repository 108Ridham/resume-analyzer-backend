import re
from collections import Counter

# ─── Curated Technical and Leadership Whitelist ───────────────────────────────
TECHNICAL_AND_LEADERSHIP_KEYWORDS = {
    # --- Programming Languages ---
    "python", "java", "c++", "c#", "csharp", "javascript", "typescript", "html", "css", "sql", "mysql", "postgresql", "mongodb",
    "rust", "go", "golang", "ruby", "php", "scala", "kotlin", "swift", "julia", "perl", "bash", "shell", "powershell",
    "yaml", "json", "xml", "graphql", "sas", "matlab", "dart", "cobol", "fortran", "assembly", "c", "dotnet",

    # --- Libraries & Frameworks ---
    "react", "angular", "vue", "nextjs", "svelte", "django", "flask", "fastapi", "spring", "springboot", "hibernate",
    "express", "nest", "nestjs", "laravel", "rails", "jquery", "bootstrap", "tailwind", "sass", "pytorch", "tensorflow",
    "keras", "scikit", "sklearn", "pandas", "numpy", "scipy", "matplotlib", "seaborn", "nltk", "spacy", "transformers",
    "huggingface", "opencv", "junit", "pytest", "selenium", "cypress", "playwright", "webpack", "babel", "vite", "redux",
    "apollo", "prisma", "sequelize", "mongoose", "gin", "fiber", "tornado", "celery",

    # --- Databases & Stores ---
    "postgres", "oracle", "redis", "elasticsearch", "cassandra", "dynamodb", "sqlite",
    "mariadb", "neo4j", "firebase", "firestore", "snowflake", "redshift", "bigquery", "hive", "hbase", "memcached",

    # --- Cloud, DevOps, & Platforms ---
    "aws", "azure", "gcp", "docker", "kubernetes", "k8s", "jenkins", "ansible", "terraform", "vagrant", "nginx", "apache",
    "git", "github", "gitlab", "bitbucket", "ci", "cd", "cicd", "mlops", "devops", "prometheus", "grafana", "datadog",
    "sentry", "elk", "splunk", "cloudformation", "circleci", "heroku", "netlify", "vercel", "digitalocean", "linode",
    "openstack", "packer", "puppet", "chef", "istio", "helm", "argocd", "rancher",

    # --- Data Engineering & Big Data ---
    "spark", "hadoop", "kafka", "airflow", "dbt", "presto", "databricks", "flink", "beam", "storm", "superset",
    "tableau", "powerbi", "mapreduce", "pig", "sqoop", "flume", "oozie", "nifi",

    # --- AI, ML, & Data Science ---
    "nlp", "vision", "llm", "llms", "generative", "genai", "gan", "cnn", "rnn", "lstm", "regression", "classification",
    "clustering", "deeplearning", "machinelearning", "bert", "gpt", "rag", "langchain",
    "llamaindex", "pinecone", "milvus", "weaviate", "chromadb",

    # --- Key Concepts & Architectures ---
    "backend", "frontend", "fullstack", "microservices", "rest", "api", "apis", "grpc", "soap", "websocket", "oauth",
    "jwt", "serverless", "saas", "paas", "iaas", "oop", "mvc", "tdd", "bdd", "concurrency",
    "multithreading", "asynchronous", "caching", "scaling", "deployment", "monitoring", "logging", "debugging",
    "testing", "automation", "responsive", "seo", "ux", "ui", "accessibility", "security", "networking", "cryptography",
    "cybersecurity", "virtualization", "containers", "containerization", "protocols", "tcp", "ip",
    "http", "dns", "loadbalancer", "subnet", "vpc", "firewall", "gateway",

    # --- Leadership, Management, & Power Words ---
    "lead", "leader", "leadership", "manage", "manager", "management", "direct", "director", "coordinate",
    "coordination", "mentor", "mentorship", "coach", "coaching", "superise", "supervisor", "supervision",
    "spearhead", "spearheaded", "orchestrate", "orchestrated", "head", "headed", "guide", "guided", "guidance",
    "strategy", "strategic", "strategize", "roadmap", "deliver", "delivery", "deliverable", "deliverables",
    "collaborate", "collaboration", "collaborative", "partner", "partnership", "stakeholder", "stakeholders",
    "agile", "scrum", "sprint", "sprints", "project", "projects", "program", "programs", "product", "products",
    "portfolio", "budget", "budgeting", "resource", "resources", "team", "teams", "hire", "hiring", "train",
    "training", "initiate", "initiated", "initiation", "execution", "execute", "executing", "executed", "oversaw",
    "oversee", "supervise", "supervised", "coordinate", "coordinated", "manage", "managed", "directed", "directing"
}


# ─── Curated power action verbs ───────────────────────────────────────────────
ACTION_VERBS = [
    # Leadership
    "led", "managed", "directed", "supervised", "oversaw", "coordinated",
    "spearheaded", "orchestrated", "headed", "guided", "mentored", "coached",
    # Development / building
    "built", "developed", "designed", "architected", "engineered", "created",
    "implemented", "deployed", "launched", "established", "founded", "initiated",
    # Improvement
    "improved", "optimized", "enhanced", "streamlined", "accelerated", "upgraded",
    "refactored", "automated", "reduced", "eliminated", "resolved", "fixed",
    # Analysis / research
    "analyzed", "researched", "investigated", "evaluated", "assessed", "audited",
    "identified", "diagnosed", "measured", "tracked", "monitored", "reviewed",
    # Collaboration
    "collaborated", "partnered", "liaised", "facilitated", "supported", "assisted",
    # Achievement
    "achieved", "delivered", "exceeded", "surpassed", "generated", "increased",
    "grew", "scaled", "expanded", "boosted", "saved", "secured", "won",
    # Communication
    "presented", "communicated", "documented", "authored", "wrote", "trained",
]


# ─── Missing keywords (JD vs Resume) ────────────────────────────────────────
def find_missing_keywords(resume_text: str, jd_text: str, top_n: int = 15) -> list:
    """
    Extract genuine technical and leadership keywords from the JD that are absent from the resume.
    Uses a whitelist approach to only keep relevant terms.
    """
    token_pattern = r'\b[a-zA-Z0-9\+\#\-\.]+\b'
    
    jd_words = re.findall(token_pattern, jd_text.lower())
    jd_words = [w for w in jd_words if w in TECHNICAL_AND_LEADERSHIP_KEYWORDS]

    resume_words = set(re.findall(token_pattern, resume_text.lower()))

    if not jd_words:
        return []

    # Rank by JD frequency; return only those absent from the resume
    jd_counter = Counter(jd_words)
    missing = [
        word for word, _ in jd_counter.most_common()
        if word not in resume_words
    ]

    return missing[:top_n]

    return missing[:top_n]


# ─── Action verb detection ────────────────────────────────────────────────────
def detect_action_verbs(raw_text: str) -> dict:
    """Find which action verbs from our list appear in the resume."""
    text_lower = raw_text.lower()
    found = []
    missing = []

    for verb in ACTION_VERBS:
        pattern = r'\b' + re.escape(verb) + r'\b'
        if re.search(pattern, text_lower):
            found.append(verb)
        else:
            missing.append(verb)

    count = len(found)
    # Score: 0–10 verbs → scale to 100
    score = min(round((count / 10) * 100), 100)

    return {
        "found": found,
        "found_count": count,
        "total_checked": len(ACTION_VERBS),
        "score": score,          # 0–100
    }


# ─── Resume length check ──────────────────────────────────────────────────────
def check_resume_length(word_count: int) -> dict:
    """Categorise the resume word count."""
    if word_count < 300:
        status = "too_short"
        label = "Too Short"
        advice = "Add more detail to experience, projects, and skills sections."
        score = 40
    elif word_count <= 800:
        status = "ideal"
        label = "Ideal Length"
        advice = "Your resume length is within the ideal range for ATS systems."
        score = 100
    elif word_count <= 1200:
        status = "slightly_long"
        label = "Slightly Long"
        advice = "Consider trimming less relevant details to improve readability."
        score = 70
    else:
        status = "too_long"
        label = "Too Long"
        advice = "Resume is too long. Aim for 1–2 pages (300–800 words)."
        score = 30

    return {
        "word_count": word_count,
        "status": status,
        "label": label,
        "advice": advice,
        "score": score,          # 0–100
    }


# ─── Formatting checks ────────────────────────────────────────────────────────
def formatting_check(raw_text: str, pdf_links: list = None) -> dict:
    """
    Heuristic checks for ATS-friendly formatting.
    Returns a list of check results and an overall score.
    """
    checks = []

    # 1. Bullet points – lines starting with common bullet markers
    bullet_lines = len(re.findall(r'(?m)^[\s]*[•\-\*\u2022\u25cf]', raw_text))
    checks.append({
        "name": "Bullet points used",
        "passed": bullet_lines >= 3,
        "detail": f"{bullet_lines} bullet lines detected"
            if bullet_lines >= 3
            else "Too few bullet points — ATS prefers structured lists",
    })

    # 2. Contact info present (email address)
    has_email = bool(re.search(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', raw_text))
    checks.append({
        "name": "Email address present",
        "passed": has_email,
        "detail": "Email detected" if has_email else "No email found — add contact info",
    })

    # 3. Phone number present
    has_phone = bool(re.search(r'(\+?\d[\d\s\-\(\)]{7,}\d)', raw_text))
    checks.append({
        "name": "Phone number present",
        "passed": has_phone,
        "detail": "Phone number detected" if has_phone else "No phone number found",
    })

    # 4. Avoid excessive ALL-CAPS (more than 5 all-caps words outside headers)
    all_caps_words = re.findall(r'\b[A-Z]{3,}\b', raw_text)
    # filter out common legit acronyms
    legit_acronyms = {"PDF", "HTML", "CSS", "SQL", "API", "AWS", "GCP", "USA", "URL",
                      "ML", "AI", "NLP", "IOT", "REST", "JSON", "XML", "HTTP", "HTTPS"}
    excessive_caps = [w for w in all_caps_words if w not in legit_acronyms]
    caps_ok = len(excessive_caps) <= 10
    checks.append({
        "name": "No excessive ALL-CAPS text",
        "passed": caps_ok,
        "detail": "Formatting looks clean" if caps_ok
            else f"{len(excessive_caps)} all-caps words detected: {', '.join(excessive_caps[:5])}{'...' if len(excessive_caps)>5 else ''} — check if these should be lowercase",
    })

    # 5. Avoid special/unicode fancy characters
    fancy_chars = re.findall(r'[^\x00-\x7F]', raw_text)
    fancy_ok = len(fancy_chars) <= 5
    checks.append({
        "name": "Standard characters only",
        "passed": fancy_ok,
        "detail": "No problematic special characters" if fancy_ok
            else f"{len(fancy_chars)} non-ASCII characters found (e.g. {' '.join(list(set(fancy_chars))[:10])}) — replace with standard text",
    })

    # 6. URLs / LinkedIn / GitHub present
    # PDF parsers sometimes insert spaces inside URLs (e.g. "linkedin. com")
    # so collapse whitespace in a copy and search there too
    collapsed = re.sub(r'\s+', '', raw_text)
    profile_pattern = re.compile(
        r'(linkedin\.com|github\.com|https?://|www\.|portfolio\.)',
        re.IGNORECASE
    )
    has_url = bool(profile_pattern.search(raw_text)) or bool(profile_pattern.search(collapsed))
    
    # Check embedded hyperlinks (from pdf annotations) if visible text fails
    if not has_url and pdf_links:
        for link in pdf_links:
            if profile_pattern.search(link):
                has_url = True
                break
                
    checks.append({
        "name": "LinkedIn / GitHub / URL present",
        "passed": has_url,
        "detail": "Profile link detected" if has_url else "No professional profile URL found — add LinkedIn or GitHub",
    })

    passed = sum(1 for c in checks if c["passed"])
    score = round((passed / len(checks)) * 100)

    return {
        "checks": checks,
        "passed_count": passed,
        "total_checks": len(checks),
        "score": score,          # 0–100
    }


# ─── Composite ATS score ──────────────────────────────────────────────────────
def compute_ats_score(
    missing_kw_count: int,
    total_jd_kw: int,
    action_verb_score: int,
    formatting_score: int,
    length_score: int,
) -> int:
    """
    Weighted composite ATS score (0–100):
      - Keyword coverage   30%  (jd keywords present in resume)
      - Action verbs       25%
      - Formatting         25%
      - Length             20%
    """
    if total_jd_kw > 0:
        present = total_jd_kw - missing_kw_count
        keyword_score = round((present / total_jd_kw) * 100)
    else:
        keyword_score = 100

    score = (
        keyword_score     * 0.30 +
        action_verb_score * 0.25 +
        formatting_score  * 0.25 +
        length_score      * 0.20
    )
    return round(score)


# ─── Main entry point ──────────────────────────────────────────────────────────
def run_ats_analysis(raw_text: str, word_count: int, jd_text: str = "", pdf_links: list = None) -> dict:
    """Run all ATS checks and return a combined result dict."""

    missing_kw  = find_missing_keywords(raw_text, jd_text)
    av          = detect_action_verbs(raw_text)
    rl          = check_resume_length(word_count)
    fc          = formatting_check(raw_text, pdf_links)

    # Total unique JD content words (for scoring denominator) — same filter as above
    token_pattern = r'\b[a-zA-Z0-9\+\#\-\.]+\b'
    jd_all = re.findall(token_pattern, jd_text.lower())
    jd_all = [w for w in jd_all if w in TECHNICAL_AND_LEADERSHIP_KEYWORDS]
    total_jd_kw = len(set(jd_all))

    ats_score = compute_ats_score(
        missing_kw_count=len(missing_kw),
        total_jd_kw=total_jd_kw,
        action_verb_score=av["score"],
        formatting_score=fc["score"],
        length_score=rl["score"],
    )

    return {
        "ats_score": ats_score,
        "missing_keywords": missing_kw,
        "action_verbs": av,
        "resume_length": rl,
        "formatting": fc,
    }
