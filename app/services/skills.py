import re

SKILLS = [
    "python", "java", "c++", "sql", "mysql",
    "machine learning", "deep learning", "nlp",
    "data science", "pandas", "numpy",
    "tensorflow", "pytorch", "docker",
    "kubernetes", "aws", "azure",
    "react", "node js", "javascript", "html", "css"
]

SKILL_ALIASES = {
    "node js": ["nodejs", "node.js", "node js"],
    "machine learning": ["machine learning", "ml"],
    "c++": ["c++", "cplusplus", "c plus plus"],
    "deep learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
}

def extract_skills(text: str, skills_set: list):
    found = set()
    for skill in skills_set:                          # ✅ use parameter, not SKILLS
        aliases = SKILL_ALIASES.get(skill, [skill])
        for alias in aliases:
            if re.search(r'\b' + re.escape(alias) + r'\b', text):
                found.add(skill)
                break
    return list(found)

def skill_gap_analysis(resume_skills, jd_skills):
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)
    matching_skills = resume_set.intersection(jd_set)
    missing_skills = jd_set.difference(resume_set)
    return list(matching_skills), list(missing_skills)

def check_resume_sections(text: str) -> dict:        # ✅ new addition
    sections = {
        "experience": ["experience", "work history", "employment"],
        "education": ["education", "academic", "degree"],
        "skills": ["skills", "technical skills", "core competencies"],
        "projects": ["projects", "portfolio", "personal projects"],
    }
    found = {}
    for section, keywords in sections.items():
        found[section] = any(kw in text for kw in keywords)
    return found