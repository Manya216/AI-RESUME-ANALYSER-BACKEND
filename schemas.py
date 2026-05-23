from pydantic import BaseModel


class ResumeResponse(BaseModel):

    id: int

    filename: str

    score: int

    role: str

    skills: str


    class Config:

        from_attributes = True