from functools import wraps
from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from uuid import UUID
from typing import Any, TYPE_CHECKING, Annotated
from sqlmodel import Session, select
from backend.app.core.security import (
    verify_password,
    create_access_token,
    get_password_hash,
    )
import jwt
from jwt.exceptions import InvalidTokenError
from backend.app.schemas.token_schema import Token
from backend.app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from backend.app.schemas.user_schema import UserRead, CreateUserRetailer
from backend.app.core.security import oauth2_scheme
from backend.app.db.session import  get_session
from backend.app.core.role import Role
from backend.app.services.crud_service import user_crud

def role_required(allowed_roles: list[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=Depends(get_current_active_user), **kwargs):
            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Requires roles: {allowed_roles}"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator 

def get_user(db: Session, email: str, model : Role ):
        statement = select(model).where(model.email == email)
        user= db.exec(statement).first()
        if user:
            return user
        raise HTTPException(status_code=404, detail='no user')
    

def authenticate_user(db: Session, email: str, password: str, model : Role):
    user = get_user(db, email=email, model=model )
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user



async def get_current_user(
    model: Role,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db, email=email, model=model)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(model: Role):
    current_user = Depends(get_current_user(model= model))
    if getattr(current_user, "disabled", False):
        raise HTTPException(status_code=400, detail="Inactive user")    
    return current_user




async def login_for_access_token(
        model: Role,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_session), 
    ) -> Token:
        
        statement = select(model).where(model.email == form_data.username)
        user = db.exec(statement).first()
        if user and verify_password(form_data.password, user.hashed_password):
            access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
            access_token = create_access_token(
                    data={"email": user.email},
                    expires_delta=access_token_expires,
            )
            return Token(access_token=access_token, token_type="bearer")
                    
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )



async def signup_user(
        model: Role,
        user_data: CreateUserRetailer,
        db: Session = Depends(get_session),
    ) -> UserRead:
        # Check if email already exists

        statement = select(model).where(model.email == user_data.email)
        existing_user = db.exec(statement).first()
            
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
            # Hash password
        hashed_pw = get_password_hash(user_data.password)

            # Create model instance
        new_user = model(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            hashed_password=hashed_pw,
            brand = user_data.brand
            )
        user_crud.create(new_user)
        return UserRead.from_orm(new_user)



@role_required(["super"])
async def read_user(user_id: UUID, model: Role, db: Session = Depends(get_session) ): 
        user = db.get(model, user_id)
        if user:
            return UserRead.from_orm(user)
        raise HTTPException(status_code=404, detail="User not found")


    
@role_required(["super"])
async def read_users(
        model: Role,
        skip : int = 0,
        limit : int = 10,
        db: Session= Depends(get_session),
    ):
        users : Any = []
       
        statement = select(model).offset(skip).limit(limit)
        user = db.exec(statement).all()
        users.extend(user)
            
        raise HTTPException(status_code=404, detail="User not found")