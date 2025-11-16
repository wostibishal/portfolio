from backend.app.services.crud import CRUDBase
from backend.app.models.product_model import Product
from backend.app.models.rating_model import Rating
from backend.app.models.comment_model import Comment
from backend.app.models.user_model import User 

product_crud = CRUDBase(Product)
comment_crud = CRUDBase(Comment)
rating_crud = CRUDBase(Rating)
user_crud = CRUDBase(User)
