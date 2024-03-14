from fastapi import APIRouter, HTTPException, Depends
import app.api.models.user as User
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.api.schemas.role import RoleCreate, RoleRead, RoleUpdate
from app.api.models.role import Role
from app.depenencies import get_db
from app.api.security.auth import jwt_authenticator

router = APIRouter()

# Get all roles current_user: User = Depends(jwt_authenticator.get_current_user)
@router.get("/", response_model=List[RoleRead])
def get_roles(db: Session = Depends(get_db), current_admin_user: User = Depends(jwt_authenticator.get_current_admin_user)) -> List[Role]:
    roles = db.query(Role).all()
    return roles

# Get role by name
@router.get("/{name}", response_model=RoleRead)
def get_role(name: str, db: Session = Depends(get_db), current_admin_user: User = Depends(jwt_authenticator.get_current_admin_user)) -> Role:
    role = db.query(Role).filter(Role.name == name).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# Create a new role
@router.post("/", response_model=RoleRead, status_code=201)
def create_role(role: RoleCreate, db: Session = Depends(get_db), current_admin_user: User = Depends(jwt_authenticator.get_current_admin_user)) -> Role:
    try:
        new_role = Role(**role.dict())
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return new_role
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Role already exists")
    
# Update a role
@router.put("/{name}", response_model=RoleRead)
def update_role(name: str, role_update: RoleUpdate, db: Session = Depends(get_db), current_admin_user: User = Depends(jwt_authenticator.get_current_admin_user)) -> Role:
    role = db.query(Role).filter(Role.name == name).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    for key, value in role_update.dict().items():
        if value is not None:
            setattr(role, key, value)
    db.commit()
    db.refresh(role)
    return role

# Delete a role
@router.delete("/{name}", status_code=204)
def update_role(name: str, db: Session = Depends(get_db), current_admin_user: User = Depends(jwt_authenticator.get_current_admin_user)) -> None:
    role = db.query(Role).filter(Role.name == name).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    return None
    