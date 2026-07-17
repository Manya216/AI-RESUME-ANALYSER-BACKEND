import ollama
import json


client = ollama.Client(
    host="https://about-dollars-ice-train.trycloudflare.com"
)


def generate_suggestions(resume_text, job_description):

    try:

        prompt = f"""
You are an AI Resume Analyzer.

Analyze the resume against the job description.

Return ONLY valid JSON.

Format:

{{
    "matched_skills": [],
    "missing_skills": [],
    "suggestions": []
}}

Resume:

{resume_text}

Job Description:

{job_description}
"""


        response = client.chat(

            model="llama3.2",

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            options={
                "temperature":0
            }

        )


        text = response["message"]["content"]


        text = text.replace("```json", "")
        text = text.replace("```", "")


        result = json.loads(
            text.strip()
        )


        return result



    except Exception as e:

        print(
            "OLLAMA ERROR:",
            e
        )

        return {

            "matched_skills": [],

            "missing_skills": [],

            "suggestions": [
                "AI suggestions unavailable"
            ]

        }