from app.services.analyser import analyze_resume
import json

file_path = 'Resume.pdf'

job_description = """
Looking for a Python developer with SQL and Docker experience.
Must have knowledge of machine learning and deep learning.
Strong understanding of NLP and data science preferred.
Experience with numpy, pandas, and tensorflow is a plus.
"""

print("=" * 60)
print("        AI RESUME ANALYZER - TEST RUN")
print("=" * 60)

print("\n⏳ Analyzing resume... please wait\n")

try:
    result = analyze_resume(file_path, job_description)

    print("✅ ANALYSIS COMPLETE\n")

    print("-" * 40)
    print(f"📊 MATCH SCORE      : {result['match_score']}%")
    print(f"🧠 SEMANTIC SCORE   : {result['semantic_score']}%")
    print(f"🛠️  SKILL SCORE      : {result['skill_score']}%")
    print(f"📝 WORD COUNT       : {result['word_count']}")
    print("-" * 40)

    print("\n✅ MATCHING SKILLS:")
    if result['matching_skills']:
        for skill in result['matching_skills']:
            print(f"   ✔ {skill}")
    else:
        print("   None found")

    print("\n❌ MISSING SKILLS:")
    if result['missing_skills']:
        for skill in result['missing_skills']:
            print(f"   ✘ {skill}")
    else:
        print("   None — great match!")

    print("\n📋 RESUME SECTIONS DETECTED:")
    for section, present in result['resume_sections'].items():
        status = "✔" if present else "✘"
        print(f"   {status} {section.capitalize()}")

    print("\n💡 RULE-BASED SUGGESTIONS:")
    for i, suggestion in enumerate(result['suggestions'], 1):
        print(f"   {i}. {suggestion}")

    print("\n🤖 LLM ADVICE:")
    if result['llm_advice']['status'] == 'success':
        print(result['llm_advice']['advice'])
    else:
        print(f"   ⚠️ {result['llm_advice']['advice']}")

    print("\n" + "=" * 60)
    print("         FULL RAW JSON OUTPUT")
    print("=" * 60)
    print(json.dumps(result, indent=2))

except FileNotFoundError:
    print("❌ ERROR: Resume PDF not found.")
    print(f"   Path used: {file_path}")

except Exception as e:
    print(f"❌ UNEXPECTED ERROR: {e}")
    import traceback
    traceback.print_exc()