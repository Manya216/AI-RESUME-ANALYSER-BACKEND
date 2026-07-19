from ai_matcher import calculate_ai_match
from ai_suggestions import generate_suggestions


def analyser_resume(resume_text, job_description):

    print("\n===== ANALYSER =====")

    ats_score = calculate_ai_match(
        resume_text,
        job_description
    )

    print("ATS SCORE:", ats_score)

    ai_result = generate_suggestions(
        resume_text,
        job_description
    )

    print("AI RESULT:", ai_result)

    result = {

        "resume_score": ats_score,

        "semantic_match_score": ats_score,

        "matched_skills": ai_result.get(
            "matched_skills",
            []
        ),

        "missing_skills": ai_result.get(
            "missing_skills",
            []
        ),

        "suggestions": ai_result.get(
            "suggestions",
            []
        )

    }

    print("FINAL RESULT:", result)

    return result
