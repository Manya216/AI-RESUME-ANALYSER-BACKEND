from passlib.context import CryptContext

from jose import jwt, JWTError


SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"


pwd_context = CryptContext(

    schemes=["bcrypt"],

    deprecated="auto"
)


# HASH PASSWORD
def hash_password(password: str):
    password = password[:72]   # IMPORTANT FIX
    return pwd_context.hash(password)


# VERIFY PASSWORD
def verify_password(

    plain_password,

    hashed_password
):

    return pwd_context.verify(

        plain_password,

        hashed_password
    )


# CREATE JWT TOKEN
def create_access_token(data):

    return jwt.encode(

        data,

        SECRET_KEY,

        algorithm=ALGORITHM
    )


# VERIFY TOKEN
def verify_token(token):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None
        