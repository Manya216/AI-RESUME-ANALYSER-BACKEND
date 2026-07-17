from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta


# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


SECRET_KEY = "your_secret_key_here"

ALGORITHM = "HS256"



# -----------------------------
# HASH PASSWORD
# -----------------------------

def hash_password(password: str):

    # bcrypt maximum limit
    password = password[:72]

    return pwd_context.hash(password)




# -----------------------------
# VERIFY PASSWORD
# -----------------------------

def verify_password(
    plain_password: str,
    hashed_password: str
):

    plain_password = plain_password[:72]

    return pwd_context.verify(
        plain_password,
        hashed_password
    )




# -----------------------------
# CREATE JWT TOKEN
# -----------------------------

def create_access_token(data: dict):

    to_encode = data.copy()


    expire = datetime.utcnow() + timedelta(
        minutes=15
    )


    to_encode.update(
        {
            "exp": expire
        }
    )


    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )




# -----------------------------
# VERIFY JWT TOKEN
# -----------------------------

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )


        return payload


    except JWTError:

        return None
