from fastapi import APIRouter
from backend.app.schemas.user_schema import UserRead
from backend.app.schemas.token_schema import Token
from backend.app.services.user_services import (
    login_for_access_token,
    signup_user,
    read_user,
    read_users
    )
from backend.app.core.role import Role

router = APIRouter(tags=["Auth"])

router.post("/token", response_model=Token)(login_for_access_token)
router.post("/signup/{model}", response_model=UserRead)(signup_user)
router.get("/users/{user_id}", response_model=UserRead)(read_user)
router.get("/users/get/", response_model=list[UserRead])(read_users)
