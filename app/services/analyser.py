import logging
from app.services.pdf_parser import extract_text_from_pdf, extract_links_from_pdf
from app.services.preprocessing import preprocess_text
from app.services.embeddings import get_embedding
from app.services.matcher import calculate_similarity
from app.services.skills import SKILLS, extract_skills, skill_gap_analysis, check_resume_sections
from app.services.suggestions import generate_suggestions
from app.services.llm import generate_llm_suggestions
from app.services.ats_checker import run_ats_analysis

logger = logging.getLogger(__name__)

def compute_final_score(similarity_score, matching_skills, jd_skills):
    if len(jd_skills) == 0:
        skill_score = 0
    else:
        skill_score = len(matching_skills) / len(jd_skills)
    final_score = (0.7 * similarity_score) + (0.3 * skill_score)
    return final_score

def analyze_resume(file_path: str, job_description: str):

    raw_text  = extract_text_from_pdf(file_path)
    pdf_links = extract_links_from_pdf(file_path)   # ✅ hyperlink annotations
    resume_text = preprocess_text(raw_text)
    jd_text = preprocess_text(job_description)

    resume_emb = get_embedding(resume_text)
    jd_emb = get_embedding(jd_text)

    similarity_score = calculate_similarity(resume_emb, jd_emb)

    resume_skills = extract_skills(resume_text, SKILLS)
    jd_skills = extract_skills(jd_text, SKILLS)

    matching_skills, missing_skills = skill_gap_analysis(resume_skills, jd_skills)

    final_score = compute_final_score(similarity_score, matching_skills, jd_skills)
    skill_score_pct = round((len(matching_skills) / len(jd_skills)) * 100, 2) if jd_skills else 0

    suggestions = generate_suggestions(
        match_score=round(final_score * 100, 2),
        semantic_score=round(similarity_score * 100, 2),
        skill_score=skill_score_pct,
        matching_skills=matching_skills,
        missing_skills=missing_skills
    )

    sections = check_resume_sections(resume_text)

    # ✅ LLM call
    llm_output = generate_llm_suggestions(
        matching_skills=matching_skills,
        missing_skills=missing_skills,
        match_score=round(final_score * 100, 2),
        resume_sections=sections,
        job_description=job_description
    )

    # ✅ ATS analysis
    ats_result = run_ats_analysis(raw_text, len(raw_text.split()), jd_text=job_description, pdf_links=pdf_links)

    logger.info(f"Analysis done | score={round(final_score*100,2)} | matched={len(matching_skills)} skills | ats={ats_result['ats_score']}")

    return {
        "match_score": round(final_score * 100, 2),
        "semantic_score": round(similarity_score * 100, 2),
        "skill_score": skill_score_pct,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "resume_sections": sections,
        "word_count": len(raw_text.split()),
        "llm_advice": llm_output,
        "ats_analysis": ats_result,                            # ✅ new
    }