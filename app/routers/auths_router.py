from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlmodel import Session, select
import jwt

from backend.app.db.session import get_session
from backend.app.models.user_model import Costumer, Retailer, Super, User
from backend.app.schemas.user_schema import UserRead, UserCreate, UpdateUser
from backend.app.schemas.token_schema import Token
from backend.app.core.security import (
    get_current_active_user,
    get_password_hash,
    verify_password,
    create_access_token,
)
from backend.app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.services.user_services import role_required


router = APIRouter(tags=["Auth"])

@router.post("/admin", response_model= UserRead)
async def Admin_signup(user_data: UserCreate, db: Session = Depends(get_session)):
    # check if username already exists
    statement = select(Super).where(Super.email == user_data.email)
    existing_user = db.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # hash password and create user
    hashed_pw = get_password_hash(user_data.password)
    new_user = Super(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashed_password=hashed_pw,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserRead.from_orm(new_user)

@router.post("/signup", response_model= UserRead)
async def Costuemr_signup(user_data: UserCreate, db: Session = Depends(get_session)):
    # check if username already exists
    statement = select(Costumer).where(Costumer.email == user_data.email)
    existing_user = db.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # hash password and create user
    hashed_pw = get_password_hash(user_data.password)
    new_user = Costumer(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashed_password=hashed_pw,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserRead.from_orm(new_user)


@router.post("/signup", response_model= UserRead)
async def Retailer_signup(user_data: UserCreate, db: Session = Depends(get_session)):
    # check if username already exists
    statement = select(Retailer).where(Retailer.email == user_data.email)
    existing_user = db.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # hash password and create user
    hashed_pw = get_password_hash(user_data.password)
    new_user = Retailer(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashed_password=hashed_pw,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserRead.from_orm(new_user)



@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
    ):
    statement = select(User).where(User.email == form_data.username)
    user = db.exec(statement).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
 

@router.get("/users/{user_id}", response_model=UserRead)
@role_required(['admin'])
def read_user(user_id: str, db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.from_orm(user)




@router.get("/users/", response_model=list[UserRead])
@role_required(["admin"])
async def read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
):
    users = db.exec(select(User).offset(skip).limit(limit)).all()
    return [UserRead.from_orm(user) for user in users]    



@router.get("/me/", response_model=UserRead)
@role_required(["admin", "costumer", "retailer"])
async def read_current_user(
    current_user: User = Depends(get_current_active_user),
):
    if getattr(current_user, "disabled", False):
        raise HTTPException(status_code=400, detail="no user is inactive")
    return UserRead.from_orm(current_user)


@router.put("/update/", response_model=UpdateUser)
@role_required(["admin"])
async def update_user( 
    User_data: UpdateUser,
    db: Session = Depends(get_session),
    ):
    statement = select(User).where( User.id == User_data.id)
    user = db.exec(statement).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User dose not exist",
        )
    Updated_user = user(
        first_name=User_data.first_name,
        last_name=User_data.last_name,
        email=User_data.email,
        password=get_password_hash(User_data.password),
        is_active= User_data.is_active,
        had_strike = User_data.had_strike,
        strike = User_data.strike,
        brand = User_data.brand,
    )
    db.add(Updated_user)
    db.commit()
    db.refresh(Updated_user)
    return UpdateUser.from_orm(Updated_user)
