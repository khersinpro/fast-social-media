from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.api.schemas.user import UserCreate, UserRead, UserUpdate
from app.api.schemas.token import Token
from app.api.models.user import User
from app.depenencies import get_db
from app.api.security.auth import jwt_authenticator 
router = APIRouter()

# Login route
@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = jwt_authenticator.authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = jwt_authenticator.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user
@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(jwt_authenticator.get_current_user)):
    return current_user

# Get user by id    
@router.get('/id/{user_id}', response_model=UserRead)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> User: 
    finded_user = db.query(User).filter(User.id == user_id).first()
    if finded_user is None:
        raise HTTPException(status_code=404, detail=f'User with id {user_id} not found')
    return finded_user

# Get user by email
@router.get('/email/{email}', response_model=UserRead)
def get_user_by_email(email: str, db: Session = Depends(get_db)) -> User:
    finded_user = db.query(User).filter(User.email == email).first()
    if finded_user is None:
        raise HTTPException(status_code=404, detail=f'User with email {email} not found')
    return finded_user

# Get all users
@router.get('/', response_model=List[UserRead])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[User]:
    user_list = db.query(User).offset(skip).limit(limit).all()
    return user_list

# Create user
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
        print(err)
        raise HTTPException(status_code=400, detail=f'User with email {user.email} already exists')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# Update user
@router.put('/{user_id}', response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(jwt_authenticator.get_current_user)) -> User:
    finded_user = db.query(User).filter(User.id == user_id).first()
    if finded_user is None:
        raise HTTPException(status_code=404, detail=f'User with id {user_id} not found')
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="You don't have permission to access this resource")
    try:
        for key, value in user.dict().items():
            if value is not None:
                setattr(finded_user, key, value)
        db.commit()
        db.refresh(finded_user)
        return finded_user
    except IntegrityError as err:
        raise HTTPException(status_code=400, detail=f'User with email {user.email} already exists')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# Delete user
@router.delete('/{user_id}', status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(jwt_authenticator.get_current_user)):
    finded_user = db.query(User).filter(User.id == user_id).first()
    if finded_user is None:
        raise HTTPException(status_code=404, detail=f'User with id {user_id} not found')
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="You don't have permission to access this resource")
    db.delete(finded_user)
    db.commit()
    return None

