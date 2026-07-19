import ollama
import json
import re
SKILL_SYNONYMS = {

    "object oriented programming": [
        "oops",
        "oop",
        "object oriented programming",
        "object-oriented programming",
        "object oriented design",
        "ood"
    ],


    "api integration": [
        "api integration",
        "apis",
        "api",
        "rest api",
        "rest apis",
        "restful api",
        "restful apis"
    ],


    "data structures and algorithms": [
        "dsa",
        "data structures",
        "data structures and algorithms",
        "algorithms"
    ],


    "jwt authentication": [
        "jwt",
        "jwt authentication",
        "json web token"
    ],


    "crud operations": [
        "crud",
        "create read update delete",
        "crud operations"
    ]

}


# ==================================
# NORMALIZE SKILLS
# ==================================
def normalize_skill(skill):

    skill = skill.lower().strip()


    for main_skill, aliases in SKILL_SYNONYMS.items():

        for alias in aliases:

            if alias in skill:

                return main_skill


    return skill





# ==================================
# DIRECT RESUME SKILL DETECTION
# ==================================

def extract_resume_skills_direct(resume_text):


    text = resume_text.lower()



    skills = {


        "jwt authentication":[
            "jwt",
            "jwt authentication"
        ],


        "crud operations":[
            "crud",
            "crud operations"
        ],


        "object oriented programming":[
            "oops",
            "oop",
            "object oriented programming",
            "object-oriented programming"
        ],


        "data structures":[
            "dsa",
            "data structure",
            "data structures",
            "data structures and algorithms"
        ],


        "rest api":[
            "rest api",
            "rest apis",
            "restful api"
        ],


        "database management systems":[
            "dbms",
            "database management systems"
        ],


        "python":[
            "python"
        ],


        "fastapi":[
            "fastapi"
        ],


        "sql":[
            "sql",
            "mysql"
        ],


        "react":[
            "react",
            "reactjs"
        ],


        "javascript":[
            "javascript",
            "js"
        ],


        "html":[
            "html",
            "html5"
        ],


        "css":[
            "css",
            "css3"
        ],


        "git":[
            "git",
            "github"
        ]

    }



    found=[]



    for skill,aliases in skills.items():

        for alias in aliases:

            if alias in text:

                found.append(skill)

                break



    return found







# ==================================
# VERIFY MATCHING
# ==================================

def verify_skill_matching(result, resume_text):


    ollama_resume_skills = [

        normalize_skill(x)

        for x in result.get(
            "resume_skills_extracted",
            []
        )

    ]



    direct_resume_skills = extract_resume_skills_direct(
        resume_text
    )



    # Combine both

    resume_skills = list(
        set(
            ollama_resume_skills
            +
            direct_resume_skills
        )
    )



    job_skills = [

        normalize_skill(x)

        for x in result.get(
            "job_skills_extracted",
            []
        )

    ]



    matched=[]

    missing=[]



    for job_skill in job_skills:


        found=False



        for resume_skill in resume_skills:



            if (

                job_skill == resume_skill

                or

                job_skill in resume_skill

                or

                resume_skill in job_skill

            ):

                found=True
                break




        if found:

            matched.append(job_skill)


        else:

            missing.append(job_skill)




    result["matched_skills"]=list(
        dict.fromkeys(matched)
    )


    result["missing_skills"]=list(
        dict.fromkeys(missing)
    )



    return result







# ==================================
# MAIN FUNCTION
# ==================================

def generate_suggestions(
        resume_text,
        job_description
):


    try:


        prompt=f"""

You are an ATS skill extractor.

Extract only technical skills.

Do NOT decide missing skills.

Python will compare skills.

Return JSON only.


FORMAT:

{{
"resume_skills_extracted":[],
"job_skills_extracted":[],
"matched_skills":[],
"missing_skills":[],
"suggestions":[]
}}


RESUME:

{resume_text}


JOB DESCRIPTION:

{job_description}

"""



        response = ollama.chat(

            model="llama3.2",

            format="json",

            messages=[

                {
                    "role":"user",
                    "content":prompt
                }

            ],


            options={

                "temperature":0

            }

        )



        content=response["message"]["content"]



        print("\nOLLAMA RAW RESPONSE:")
        print(content)




        content=content.replace(
            "```json",
            ""
        )


        content=content.replace(
            "```",
            ""
        )



        match=re.search(
            r"\{.*\}",
            content,
            re.DOTALL
        )


        if match:

            content=match.group(0)



        result=json.loads(content)



        # FINAL PYTHON VERIFICATION

        result=verify_skill_matching(
            result,
            resume_text
        )



        print("\nFINAL VERIFIED RESULT:")
        print(result)




        if result["missing_skills"]:


            suggestions=[

                "Consider adding these missing skills: "
                +
                ", ".join(
                    result["missing_skills"]
                )

            ]


        else:


            suggestions=[

                "Resume skills match well with the job requirements."

            ]





        return {


            "matched_skills":
            result["matched_skills"],



            "missing_skills":
            result["missing_skills"],



            "suggestions":
            suggestions

        }





    except Exception as e:


        print(
            "OLLAMA ERROR:",
            e
        )


        return {

            "matched_skills":[],

            "missing_skills":[],

            "suggestions":[
                "AI suggestions unavailable"
            ]

        }
