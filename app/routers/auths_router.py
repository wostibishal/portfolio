from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlmodel import Session, select
import jwt
# from jwt.exceptions import InvalidTokenError
# from fastapi.responses import JSONResponse
from backend.app.db.session import get_session
from backend.app.models.user_model import User
from backend.app.schemas.user_schema import UserRead, UserCreate
from backend.app.schemas.token_schema import Token
from backend.app.core.security import (
    get_current_active_user,
    get_password_hash,
    verify_password,
    create_access_token,
    # create_refresh_token,
)
from backend.app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.core.role import role_required


router = APIRouter(tags=["Auth"])


@router.post("/signup", response_model= UserRead)
async def signup(user_data: UserCreate, db: Session = Depends(get_session)):
    # check if username already exists
    statement = select(User).where(User.email == user_data.email)
    existing_user = db.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # hash password and create user
    hashed_pw = get_password_hash(user_data.password)
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        role=user_data.role,
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
    # refresh_token = create_refresh_token(data={"sub": user.email})
    # response = JSONResponse(content={
    #     "access_token": access_token,
    #     "token_type": "bearer"
    # })
    # response.set_cookie(
    #     key="refresh_token",
    #     value=refresh_token,
    #     httponly=True,
    #     secure=True,
    #     samesite="lax",
    #     max_age=int(REFRESH_TOKEN_EXPIRE_DAYS) * 24 * 3600
    # )
    # return Token(access_token=access_token, token_type="bearer"), response





###### this part is commented for refresh token implementation ######


# @router.post("/refresh")
# def refresh_access_token(request: Request):
#     refresh_token = request.cookies.get("refresh_token")
#     if not refresh_token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")

#     try:
#         payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
#         if payload.get("type") != "refresh":
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
#     except InvalidTokenError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

#     new_access_token = create_access_token(data={"sub": payload.get("sub")})
#     return Token(access_token=new_access_token, token_type="bearer")




########### this is implementation  error ###########

# @router.post("/token", response_model=Token)
# def login(
#     form_data: loginSchema,
#     db: Session = Depends(get_session),
#     ):
#     statement = select(usermodule).where(usermodule.email == form_data.email)
#     user = db.exec(statement).first()

#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
#     access_token = create_access_token(
#         data={"sub": user.email}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")



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