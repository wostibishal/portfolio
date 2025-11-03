from backend.app.services.crud import CRUDBase
from backend.app.models.item_model import Item, Rating, Comment 

item_crud = CRUDBase(Item)
comment_crud = CRUDBase(Comment)
rating_crud = CRUDBase(Rating)
