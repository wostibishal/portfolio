
# from fastapi import APIRouter
# from backend.app.services.product_services import (
#     create_product,
#     products,
#     product,
#     read_my_products,
#     retailer_products,
#     update_product,
#     delete_product,

# )
# from backend.app.schemas.product_schema import Read_product, Create_product, Update_product, Delete_product
# from backend.app.models.user_model import Retailer




# router = APIRouter(tags=["products"])

# router.post("/create/",response_model=Read_product)(create_product)
# router.post("/products/",response_model=Read_product)(products(Retailer))
# router.post("/my_products/",response_model=Read_product)(read_my_products(Retailer))
# router.post("/product/{product_id}",response_model=Read_product)(product(Retailer))
# router.post("/products/{retailer_id}",response_model=Read_product)(retailer_products(Retailer))
# router.post("/update/{product_id}",response_model=Read_product)(update_product(Retailer))
# router.post("/delete/{product_id}",response_model=Read_product)(delete_product(Retailer))

