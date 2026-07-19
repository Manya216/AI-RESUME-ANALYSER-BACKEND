from sentence_transformers import SentenceTransformer, util


# Load once
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)



# Skill normalization dictionary

SKILL_ALIASES = {

    "data structures": [
        "dsa",
        "data structure",
        "data structures",
        "data structure and algorithms",
        "data structures and algorithms",
        "data structure & algorithms",
        "data structures & algorithms"
    ],


    "object oriented programming": [
        "oops",
        "oop",
        "object oriented programming",
        "object-oriented programming",
        "object oriented design"
    ],


    "javascript": [
        "javascript",
        "javascript es6",
        "js"
    ],


    "python": [
        "python"
    ],


    "c++": [
        "c++",
        "cpp",
        "c plus plus"
    ],


    "sql": [
        "sql",
        "mysql",
        "postgresql",
        "database sql"
    ],


    "rest api": [
        "rest api",
        "restful api",
        "rest APIs",
        "api development"
    ],


    "database management": [
        "dbms",
        "database management systems",
        "database management"
    ],


    "react": [
        "react",
        "reactjs",
        "react.js"
    ],


    "html": [
        "html",
        "html5"
    ],


    "css": [
        "css",
        "css3"
    ],


    "fastapi": [
        "fastapi"
    ],


    "git": [
        "git",
        "github",
        "version control"
    ],


    "jwt authentication": [
        "jwt",
        "jwt authentication",
        "authentication"
    ],


    "crud operations": [
        "crud",
        "crud operations"
    ]

}



def extract_skills(text):

    text = text.lower()

    extracted = set()


    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if alias.lower() in text:

                extracted.add(skill)

                break


    return extracted





def calculate_ai_match(resume_text, job_description):


    try:


        if not resume_text or not job_description:

            return 0



        resume_text = resume_text.lower()

        job_description = job_description.lower()



        # --------------------------
        # Semantic similarity
        # --------------------------


        embeddings = model.encode(

            [
                resume_text,
                job_description
            ],

            convert_to_tensor=True

        )


        semantic_score = float(

            util.cos_sim(

                embeddings[0],
                embeddings[1]

            )[0][0]

        )



        semantic_score = max(

            semantic_score,
            0

        )



        semantic_percentage = semantic_score * 100





        # --------------------------
        # Skill matching
        # --------------------------


        resume_skills = extract_skills(
            resume_text
        )


        jd_skills = extract_skills(
            job_description
        )



        if len(jd_skills) > 0:


            matched = len(

                resume_skills.intersection(
                    jd_skills
                )

            )


            skill_percentage = (

                matched /

                len(jd_skills)

            ) * 100


        else:


            skill_percentage = 0





        # --------------------------
        # Final ATS score
        # --------------------------

        final_score = (

            0.5 * semantic_percentage

            +

            0.5 * skill_percentage

        )



        return round(

            min(
                final_score,
                100
            ),

            2

        )




    except Exception as e:


        print(
            "AI MATCH ERROR:",
            e
        )


        return 0
