from datetime import timedelta
from fastapi import Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlmodel import Session, select
from pydantic import EmailStr
from backend.app.core.security import (
    RoleChecker,
    create_access_token
)
from backend.app.schemas.token_schema import Token
from backend.app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.schemas.user_schema import (
    UserCreateBase, DisplayUser, SuperDisplayUser, 
    RetailerRegister, ReadUser, SuperUpdate,
    DisplayRetailer,UpdatePassword
)
from backend.app.db.session import get_session
from backend.app.core.enum import Role
from backend.app.util.crud_service import user_crud
from backend.app.models.user_model import User
from backend.app.models.user_model import RetailerProfile
from backend.app.util.user.auth_user import authenticate_user
from backend.app.util.user.get_current_active_user import get_current_active_user
from backend.app.util.user.get_password_hash import get_password_hash




async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_session), 
    ) -> Token:
        
        user = authenticate_user(db, email=form_data.username, password=form_data.password)

        if user:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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


async def signup_costumer(
        user_data: UserCreateBase,
        db: Session = Depends(get_session),
    ) -> DisplayUser:
        statement = select(User).where(User.email == user_data.email)
        existing_user = db.exec(statement).first()
            
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        hashed_pw = get_password_hash(user_data.password)
        user_create_data = user_data.model_dump() 
        user_create_data["hashed_password"] = hashed_pw
        user_create_data["role"] = Role.COSTUMER.value 

        new_user = user_crud.create(db=db, obj_in=user_create_data) 
        return DisplayUser.model_validate(new_user)


async def signup_retailer(
        user_data: RetailerRegister,
        db: Session = Depends(get_session),
    ) -> DisplayRetailer:
        statement = select(User).where(User.email == user_data.email)
        existing_user = db.exec(statement).first()
            
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        hashed_pw = get_password_hash(user_data.password)
        
        user_create_data = user_data.model_dump(exclude={"brand_name"})
        user_create_data["hashed_password"] = hashed_pw
        user_create_data["role"] = Role.RETAILER.value
        user_create_data["is_active"] = False 

        new_user = user_crud.create(db=db, obj_in=user_create_data)

        retailer_profile_data = {
            "user_id": new_user.id,
            "brand_name": user_data.brand_name,
        }
        
        new_profile = RetailerProfile(**retailer_profile_data)
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        
        new_user.retailer_profile = new_profile

        return DisplayRetailer.model_validate(new_user)


async def signup_super(
        user_data: UserCreateBase,
        db: Session = Depends(get_session),
    ) -> SuperDisplayUser:
        statement = select(User).where(User.email == user_data.email)
        existing_user = db.exec(statement).first()
            
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        hashed_pw = get_password_hash(user_data.password)
        user_create_data = user_data.model_dump() 
        user_create_data["hashed_password"] = hashed_pw
        user_create_data["role"] = Role.SUPER.value
        
        new_user = user_crud.create(db=db, obj_in=user_create_data)
        
        return SuperDisplayUser.model_validate(new_user)


async def admin_read_user( 
    email: EmailStr = Path(...), 
    db: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker(["super"])), 
) -> SuperDisplayUser: 
        if current_user.role == Role.SUPER:
            statement = select(User).where(User.email == email)
            user = db.exec(statement).first() 

            if user:
                return SuperDisplayUser.model_validate(user)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


async def admin_read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker(["super"])),
) -> list[SuperDisplayUser]:

    if current_user.role == Role.SUPER:
        statement = select(User).offset(skip).limit(limit)
        users = db.exec(statement).all()

        if users:
            return [SuperDisplayUser.model_validate(u) for u in users]

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )

async def admin_update_user(
    data: SuperUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker(["super"])),
) -> SuperDisplayUser:
    if current_user.role == Role.SUPER:
        statement = (select(User).where(User.email == data.email))
        user = db.exec(statement).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email doesn't exist",
            )
    
        user_update_data = data.model_dump(exclude_unset=True) 

        if "password" in user_update_data:
            hash_password = get_password_hash(user_update_data["password"])
            user_update_data["hashed_password"] = hash_password
            del user_update_data["password"] 

        if user.role.value == Role.RETAILER.value:
            retailer_fields = ["brand_name", "strike_count", "is_verified"]
            
            if user.retailer_profile:
                for field in retailer_fields:
                    if field in user_update_data:
                        setattr(user.retailer_profile, field, user_update_data[field])
                        del user_update_data[field]
                
                db.add(user.retailer_profile)

        update_user = user_crud.update(db=db, db_obj=user, obj_in=user_update_data)
        
        db.commit()
        db.refresh(update_user)
        
        return SuperDisplayUser.model_validate(update_user)
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )

def update_password(
    data: UpdatePassword,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)  
) -> ReadUser:
    user = db.exec(select(User).where(User.email == current_user.email)).first()
    user_update_data = data.model_dump()
    