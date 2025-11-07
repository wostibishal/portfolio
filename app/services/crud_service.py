from backend.app.services.crud import CRUDBase
from backend.app.models.product_model import product, Rating, Comment 

product_crud = CRUDBase(product)
comment_crud = CRUDBase(Comment)
rating_crud = CRUDBase(Rating)
