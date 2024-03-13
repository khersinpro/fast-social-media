from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.api.schemas.user import UserCreate, User as UserRead
from app.api.models.user import User
from app.depenencies import get_db
from app.api.security.auth import jwt_authenticator
from app.api.schemas.token import Token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Get the access token for the user
    """
    user = jwt_authenticator.authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = jwt_authenticator.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(jwt_authenticator.get_current_user)):
    """
    Get the current user
    """
    return current_user
    
@router.get('/id/{user_id}', response_model=UserRead)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> User: 
    finded_user = db.query(User).filter(User.id == user_id).first()
    if finded_user is None:
        raise HTTPException(status_code=404, detail=f'User with id {user_id} not found')
    return finded_user

@router.get('/email/{email}', response_model=UserRead)
def get_user_by_email(email: str, db: Session = Depends(get_db)) -> User:
    finded_user = db.query(User).filter(User.email == email).first()
    if finded_user is None:
        raise HTTPException(status_code=404, detail=f'User with email {email} not found')
    return finded_user

@router.get('/', response_model=List[UserRead])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[User]:
    user_list = db.query(User).offset(skip).limit(limit).all()
    return user_list

@router.post('/', response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    try:
        hashed_password = User.get_password_hash(user.password)
        db_user = User(email=user.email, username=user.username, password=hashed_password, firstname=user.firstname, lastname=user.lastname)
        # add the user to the database session
        db.add(db_user)
        # commit the changes to the database
        db.commit()
        # refresh the user instance to populate the id field
        db.refresh(db_user)
        return db_user
    except IntegrityError as err:
        raise HTTPException(status_code=400, detail=f'User with email {user.email} already exists')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
