import os
import time

from fastapi import FastAPI, File, UploadFile, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal, engine, Base
from models import Resume, User

from extract import extract_from
from analyser import analyser_resume

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)

# CREATE TABLES
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_origin_regex=r"https://.*\.netlify\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# AUTH USER
def get_current_user(authorization: str = Header(None)):
    if not authorization:
        return None

    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)

    return payload if payload else None

# =========================
# REQUEST MODELS (IMPORTANT FIX)
# =========================

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# =========================
# ROUTES
# =========================

@app.get("/")
def home():
    return {"message": "AI Resume Analyzer API"}

# -------------------------
# SIGNUP (FIXED)
# -------------------------
@app.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == data.email).first()

    if existing:
        return {"message": "User already exists"}

    user = User(
        username=data.username,
        email=data.email,
        password=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Signup successful"}

# -------------------------
# LOGIN (FIXED)
# -------------------------
@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        return {"message": "Invalid email"}

    if not verify_password(data.password, user.password):
        return {"message": "Invalid password"}

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# -------------------------
# UPLOAD RESUME
# -------------------------
@app.post("/upload")
async def upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if not current_user:
        return {"message": "Please login first"}

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{int(time.time())}_{file.filename}"

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    resume_text = extract_from(file_path)
    analysis = analyser_resume(resume_text)

    user_email = current_user["sub"]

    new_resume = Resume(
        filename=file.filename,
        score=analysis["resume_score"],
        role=analysis["predicted_role"],
        skills=", ".join(analysis["skills_found"]),
        user_email=user_email
    )

    db.add(new_resume)
    db.commit()

    return {
        "analysis": analysis
    }

# -------------------------
# GET RESUMES
# -------------------------
@app.get("/resumes")
def get_resumes(db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    if not current_user:
        return []

    return db.query(Resume).filter(
        Resume.user_email == current_user["sub"]
    ).all()