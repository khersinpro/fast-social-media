from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.api.schemas.user import UserCreate, User as UserRead
from app.api.models.user import User
from app.depenencies import get_db

router = APIRouter()

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
        db_user = User(email=user.email, password=hashed_password, firstname=user.firstname, lastname=user.lastname)
        # add the user to the database session
        db.add(db_user)
        # commit the changes to the database
        db.commit()
        # refresh the user instance to populate the id field
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f'User with email {user.email} already exists')
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")