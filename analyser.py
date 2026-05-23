import re


# -----------------------------
# ALL SKILLS DATABASE
# -----------------------------

skills_db = [

    "python",
    "c++",
    "java",
    "html",
    "css",
    "javascript",
    "react",
    "fastapi",
    "sql",
    "mysql",
    "mongodb",
    "machine learning",
    "git",
    "docker",
    "numpy",
    "pandas",
    "nodejs",
    "express",
    "aws",
    "firebase",
    "tailwind",
    "bootstrap"
]


# -----------------------------
# ROLE-WISE SKILLS
# -----------------------------

frontend_skills = [

    "html",
    "css",
    "javascript",
    "react",
    "tailwind",
    "bootstrap"
]


backend_skills = [

    "python",
    "fastapi",
    "sql",
    "mysql",
    "mongodb",
    "nodejs",
    "express"
]


ml_skills = [

    "machine learning",
    "numpy",
    "pandas"
]


# -----------------------------
# MAIN ANALYZER FUNCTION
# -----------------------------

def analyser_resume(text):

    text = text.lower()

    found_skills = []


    # -----------------------------
    # SKILL DETECTION
    # -----------------------------

    for skill in skills_db:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):

            found_skills.append(skill)


    # -----------------------------
    # SECTION DETECTION
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

        "certification" in text

        or

        "certificate" in text
    )


    github_present = (

        "github.com" in text
    )


    linkedin_present = (

        "linkedin.com" in text
    )


    # -----------------------------
    # REALISTIC ATS SCORE
    # -----------------------------

    score = 0


    # SKILLS SCORE (MAX 30)

    skills_score = min(

        (len(found_skills) / 10) * 30,

        30
    )

    score += skills_score


    # PROJECTS SCORE

    if projects_present:

        score += 20


    # EXPERIENCE SCORE

    if experience_present:

        score += 20


    # CERTIFICATIONS SCORE

    if certification_present:

        score += 10


    # GITHUB SCORE

    if github_present:

        score += 10


    # LINKEDIN SCORE

    if linkedin_present:

        score += 10


    # -----------------------------
    # PENALTIES
    # -----------------------------

    if len(found_skills) < 4:

        score -= 10


    if not projects_present:

        score -= 15


    if not github_present:

        score -= 5


    # -----------------------------
    # LIMIT SCORE
    # -----------------------------

    score = max(0, min(round(score), 100))


    # -----------------------------
    # ROLE DETECTION
    # -----------------------------

    frontend_count = 0

    backend_count = 0

    ml_count = 0


    for skill in frontend_skills:

        if skill in found_skills:

            frontend_count += 1


    for skill in backend_skills:

        if skill in found_skills:

            backend_count += 1


    for skill in ml_skills:

        if skill in found_skills:

            ml_count += 1


    role = "General Software Developer"


    max_count = max(

        frontend_count,

        backend_count,

        ml_count
    )


    if max_count == frontend_count and max_count != 0:

        role = "Frontend Developer"


    elif max_count == backend_count and max_count != 0:

        role = "Backend Developer"


    elif max_count == ml_count and max_count != 0:

        role = "ML Engineer"


    # -----------------------------
    # SUGGESTIONS
    # -----------------------------

    suggestions = []


    if not projects_present:

        suggestions.append(

            "Add strong projects section"
        )


   


   


    if len(found_skills) < 5:

        suggestions.append(

            "Add more technical skills"
        )


    if not certification_present:

        suggestions.append(

            "Add certifications"
        )


    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------

    return {

        "resume_score": score,

        "predicted_role": role,

        "skills_found": found_skills,

        "education_present": education_present,

        "projects_present": projects_present,

        "experience_present": experience_present,

        "certification_present": certification_present,

        "github_present": github_present,

        "linkedin_present": linkedin_present,

        "suggestions": suggestions
    }