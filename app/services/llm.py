import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate_llm_suggestions(
    matching_skills: list,
    missing_skills: list,
    match_score: float,
    resume_sections: dict,
    job_description: str
) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "advice": "LLM suggestions unavailable: GROQ_API_KEY environment variable is not set."
        }
    
    client = Groq(api_key=api_key)

    prompt = f"""
You are an expert career advisor and resume coach.

A candidate has submitted their resume for the following job:
Job Description: {job_description[:500]}

Resume Analysis Results:
- Overall Match Score: {match_score}%
- Matching Skills: {', '.join(matching_skills) if matching_skills else 'None'}
- Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}
- Resume Sections Present: {resume_sections}

Provide your response in EXACTLY this format with these EXACT section headers.
Do NOT use markdown, asterisks, bold, or any special formatting.
Use plain text only.

SUMMARY
Write 2 sentences assessing the candidate overall.

IMPROVEMENTS
1. Write first specific improvement here
2. Write second specific improvement here
3. Write third specific improvement here

PROJECTS
1. Write first project idea to cover missing skills
2. Write second project idea to cover missing skills

KEYWORDS
Keyword1
Keyword2
Keyword3
Keyword4
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert career advisor. Give specific, actionable advice in plain text only. No markdown, no asterisks, no bold formatting whatsoever."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000,
        )

        llm_response = response.choices[0].message.content
        return {
            "status": "success",
            "advice": llm_response
        }

    except Exception as e:
        return {
            "status": "error",
            "advice": f"LLM suggestions unavailable: {str(e)}"
        }