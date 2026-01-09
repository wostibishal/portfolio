from backend.app.services.crud import CRUDBase
from backend.app.models.product_model import Product
from backend.app.models.user_model import User 

product_crud = CRUDBase(Product)
user_crud = CRUDBase(User)
