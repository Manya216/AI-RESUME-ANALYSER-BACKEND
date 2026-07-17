import os
import time




from fastapi import (
    FastAPI,
    File,
    UploadFile,
    Depends,
    Form,
    Request,
    Response
)

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from pydantic import BaseModel


from database import (
    SessionLocal,
    engine,
    Base
)

from models import Resume, User


from extract import extract_from
from analyser import analyser_resume


from auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)


from chat import router as chat_router



# -----------------------------
# CREATE TABLES
# -----------------------------

try:
    Base.metadata.create_all(bind=engine)
    print("Database connected")
except Exception as e:
    print("Database connection failed:", e)



app = FastAPI()



# -----------------------------
# CHAT ROUTER
# -----------------------------

app.include_router(chat_router)




# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)




# -----------------------------
# DATABASE
# -----------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()




# -----------------------------
# CURRENT USER FROM COOKIE
# -----------------------------

def get_current_user(
    request: Request
):

    token = request.cookies.get(
        "access_token"
    )


    if not token:

        return None



    payload = verify_token(
        token
    )


    return payload




# -----------------------------
# MODELS
# -----------------------------


class SignupRequest(BaseModel):

    username:str

    email:str

    password:str




class LoginRequest(BaseModel):

    email:str

    password:str





# -----------------------------
# HOME
# -----------------------------

@app.get("/")
def home():

    return {
        "message":"AI Resume Analyzer API"
    }





# -----------------------------
# SIGNUP
# -----------------------------

@app.post("/signup")
def signup(

    data:SignupRequest,

    db:Session=Depends(get_db)

):


    existing = db.query(User).filter(
        User.email == data.email
    ).first()



    if existing:

        return {
            "message":"User already exists"
        }



    user = User(

        username=data.username,

        email=data.email,

        password=hash_password(
            data.password
        )

    )


    db.add(user)

    db.commit()

    db.refresh(user)



    return {

        "message":"Signup successful"

    }






# -----------------------------
# LOGIN
# -----------------------------

@app.post("/login")
def login(

    data:LoginRequest,

    response:Response,

    db:Session=Depends(get_db)

):


    user=db.query(User).filter(

        User.email==data.email

    ).first()



    if not user:

        return {
            "message":"Invalid email"
        }



    if not verify_password(

        data.password,

        user.password

    ):

        return {

            "message":"Invalid password"

        }




    token=create_access_token(

        {

            "sub":user.email

        }

    )




    response.set_cookie(

        key="access_token",

        value=token,

        httponly=True,

        max_age=900,

        expires=900,

        secure=False,

        samesite="lax"

    )



    return {

        "message":"Login successful"

    }







# -----------------------------
# LOGOUT
# -----------------------------

@app.post("/logout")
def logout(

    response:Response

):

    response.delete_cookie(

        "access_token"

    )


    return {

        "message":"Logged out"

    }







# -----------------------------
# UPLOAD RESUME
# -----------------------------
# -----------------------------
# UPLOAD RESUME
# -----------------------------

@app.post("/upload")
async def upload(

    file: UploadFile = File(...),

    job_description: str = Form(...),

    db: Session = Depends(get_db),

    current_user = Depends(get_current_user)

):


    if not current_user:

        return {
            "message": "Please login first"
        }




    os.makedirs(
        "uploads",
        exist_ok=True
    )



    file_path = f"uploads/{int(time.time())}_{file.filename}"



    contents = await file.read()



    with open(
        file_path,
        "wb"
    ) as f:

        f.write(contents)





    # Extract resume text

    resume_text = extract_from(

        file_path

    )





    # Analyze resume

    analysis = analyser_resume(

        resume_text,

        job_description

    )





    # -----------------------------
    # FIX SKILLS FORMAT FOR DATABASE
    # -----------------------------


    matched_skills = analysis.get(

        "matched_skills",

        []

    )



    skill_names = []



    for skill in matched_skills:


        if isinstance(skill, dict):

            skill_names.append(

                skill.get(

                    "skill",

                    ""

                )

            )


        else:

            skill_names.append(skill)





    skills_text = ", ".join(

        skill_names

    )





    # -----------------------------
    # SAVE TO DATABASE
    # -----------------------------


    new_resume = Resume(

        filename=file.filename,


        score=analysis.get(

            "resume_score",

            0

        ),


        role="AI Resume Match",


        skills=skills_text,


        user_email=current_user["sub"]

    )



    db.add(new_resume)

    db.commit()

    db.refresh(new_resume)





    return {


        "analysis": analysis,


        "resume_text": resume_text,


        "job_description": job_description

    }






# -----------------------------
# HISTORY
# -----------------------------

@app.get("/resumes")
def get_resumes(

    db:Session=Depends(get_db),

    current_user=Depends(get_current_user)

):


    if not current_user:

        return []



    resumes=db.query(Resume).filter(

        Resume.user_email==current_user["sub"]

    ).all()



    return resumes
