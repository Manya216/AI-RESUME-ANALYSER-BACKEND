from ai_matcher import calculate_ai_match

from ai_suggestions import generate_suggestions





def analyser_resume(

    resume_text,

    job_description

):


    text = resume_text.lower()





    # -----------------------------
    # SECTION CHECK
    # -----------------------------


    education_present = (

        "education" in text

    )



    projects_present = (

        "project" in text

    )



    experience_present = (

        "experience" in text

        or

        "internship" in text

    )



    certification_present = (

        "certificate" in text

        or

        "certification" in text

    )



    github_present = (

        "github.com" in text

    )



    linkedin_present = (

        "linkedin.com" in text

    )





    # -----------------------------
    # SEMANTIC MATCH
    # -----------------------------


    ai_score = calculate_ai_match(

        resume_text,

        job_description

    )





    # -----------------------------
    # OLLAMA AI SUGGESTIONS
    # -----------------------------


    ai_result = generate_suggestions(

        resume_text,

        job_description

    )





    if not isinstance(

        ai_result,

        dict

    ):

        ai_result = {}





    matched_skills = ai_result.get(

        "matched_skills",

        []

    )



    missing_skills = ai_result.get(

        "missing_skills",

        []

    )



    suggestions = ai_result.get(

        "suggestions",

        []

    )





    # -----------------------------
    # QUALITY SCORE
    # -----------------------------


    quality_score = 0



    if education_present:

        quality_score += 20



    if projects_present:

        quality_score += 20



    if experience_present:

        quality_score += 20



    if certification_present:

        quality_score += 10



    if github_present:

        quality_score += 15



    if linkedin_present:

        quality_score += 15





    # -----------------------------
    # FINAL ATS SCORE
    # -----------------------------


    skill_bonus = 0



    if isinstance(

        matched_skills,

        list

    ):

        skill_bonus = len(matched_skills) * 5





    final_score = round(

        (0.7 * ai_score)

        +

        (0.2 * quality_score)

        +

        (0.1 * skill_bonus)

    )



    final_score = min(

        final_score,

        100

    )





    return {


        "resume_score": final_score,


        "semantic_match_score": ai_score,


        "matched_skills": matched_skills,


        "missing_skills": missing_skills,


        "suggestions": suggestions,



        "education_present": education_present,


        "projects_present": projects_present,


        "experience_present": experience_present,


        "certification_present": certification_present,


        "github_present": github_present,


        "linkedin_present": linkedin_present

    }
