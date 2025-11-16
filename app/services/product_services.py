# from fastapi import Depends, HTTPException
# from backend.app.db.session import get_session
# from backend.app.schemas.product_schema import Read_product, Create_product, Update_product, Delete_product
# from sqlmodule import Session, select
# from backend.app.models.user_model import Retailer
# from backend.app.core.security import get_current_active_user

# def create_product(model):
#     async def create(
#         product_data : Create_product,
#         db: Session = Depends(get_session)
#         current_user : Retailer = Depends(get_current_active_user)
#     ):
