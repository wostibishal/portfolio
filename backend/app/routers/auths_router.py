from fastapi import APIRouter
from backend.app.schemas.user_schema import DisplayUser, DisplayRetailer, SuperDisplayUser
from backend.app.schemas.token_schema import Token
from backend.app.services.user_services import (
    login_for_access_token,
    signup_costumer,
    signup_retailer,
    signup_super,
    admin_read_user,
    admin_read_users,
    admin_update_user
    )

router = APIRouter(tags=["Auth"])

router.post("/token/", response_model=Token)(login_for_access_token)
router.post("/signup/costumer/", response_model=DisplayUser)(signup_costumer)
router.post("/signup/retailer/", response_model=DisplayRetailer)(signup_retailer)
router.post("/signup/super/", response_model=DisplayUser)(signup_super)
router.get("/user/{email}", response_model=SuperDisplayUser)(admin_read_user)
router.get("/users/", response_model=list[SuperDisplayUser])(admin_read_users)
router.put("/user/update/", response_model=SuperDisplayUser)(admin_update_user)
