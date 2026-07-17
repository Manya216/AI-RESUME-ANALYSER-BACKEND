from sentence_transformers import SentenceTransformer
from sentence_transformers import util

# Load model only once
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def calculate_ai_match(
    resume_text,
    job_description
):
    """
    Calculates semantic similarity
    between resume and job description.
    """

    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=True
    )

    job_embedding = model.encode(
        job_description,
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        resume_embedding,
        job_embedding
    )

    score = float(similarity)

    return round(score * 100, 2)