def generate_suggestions(match_score, semantic_score, skill_score,
                         matching_skills, missing_skills):
    
    suggestions = []
    
    # Low overall match
    if match_score < 50:
        suggestions.append("Your resume is not well aligned with the job description. Consider tailoring it more closely.")
    
    # Medium match
    elif match_score < 75:
        suggestions.append("Your resume is moderately aligned. Improving key areas can increase your chances.")
    
    # High match
    else:
        suggestions.append("Your resume shows strong alignment with the job requirements.")
    
    # Missing skills suggestions
    for skill in missing_skills:
        suggestions.append(f"Consider adding experience or projects related to {skill}.")
    
    # Strengths
    if matching_skills:
        suggestions.append(f"You have strong skills in: {', '.join(matching_skills)}.")
    
    # Skill coverage
    if skill_score < 50:
        suggestions.append("You are missing several required skills. Focus on improving skill coverage.")
    
    # Semantic insight
    if semantic_score < 50:
        suggestions.append("Your resume content does not strongly reflect the job role. Improve project descriptions and experience relevance.")
    
    return suggestions