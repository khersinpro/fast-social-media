from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Union
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.api.models.user import User
from app.depenencies import get_db
from app.api.schemas.token import Token, TokenData

SECRET_KEY = "51bc49c1b96f286c39b2ef7fbab6885ac993332d6ee17940d213dc0d02283c82"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

class JWTAuthenticator:
    def __init__(self, secret_key: str, algorithm: str, access_token_expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(self, data: dict) -> str:
        """
        Create a new access token with the user id as the subject and an expiration time.

        args:
        - data: dict - user data

        return:
        - str - encoded jwt token
        """
        to_encode = data.copy()
        expires_delta = timedelta(minutes=self.access_token_expire_minutes)
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def authenticate_user(self, username: str, password: str, db: Session) -> Union[User, None]:
        """
        Authenticate the user

        return:
        - User instance if authentication successful, None otherwise
        """
        user = db.query(User).filter(User.username == username).first()
        if user is None or not user.verify_password(password):
            return None
        return user

    def get_current_user(self, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
        """
        Get the current user
        """
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError as err:
            raise credentials_exception
        user = db.query(User).filter(User.username == token_data.username).first()
        if user is None:
            raise credentials_exception
        return user

jwt_authenticator = JWTAuthenticator(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)
