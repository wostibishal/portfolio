from typing import TypeVar, Type, Generic, List, Any, Dict, Union
from fastapi import HTTPException, status
from sqlmodel import Session, select, SQLModel
from uuid import UUID


ModelType = TypeVar("ModelType", bound=SQLModel) 
CreateUpdateSchemaType = TypeVar("CreateUpdateSchemaType", bound=Union[Dict[str, Any], Any]) 


class CRUDBase(Generic[ModelType]):
    """
    Generic CRUDBase class providing default methods for basic C.R.U.D. operations.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model


    def get_single(self, db: Session, id: UUID) -> ModelType:
        """Fetch a single object by its primary key (ID)."""
        statement = select(self.model).where(self.model.id == id)
        result = db.exec(statement).first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"{self.model.__name__} not found with ID: {id}"
            )
        return result

    def get_all(self, db: Session, skip: int = 0, limit: int = 10) -> List[ModelType]:
        """Fetch a list of objects with optional pagination."""
        statement = select(self.model).offset(skip).limit(limit)
        return list(db.exec(statement).all())

    def get_by_user(
        self, db: Session, user_id: UUID, skip: int = 0, limit: int = 10
    ) -> List[ModelType]:
        """Fetch objects associated with a specific user (owner_id)."""
        if not hasattr(self.model, "owner_id"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{self.model.__name__} does not have an 'owner_id' field for this query type.",
            )
        
        statement = (
            select(self.model)
            .where(self.model.owner_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return list(db.exec(statement).all())


    def create(self, db: Session, obj_in: CreateUpdateSchemaType) -> ModelType:
        """
        Create a new database object from a schema (Pydantic/SQLModel) or dict.
        
        The method handles instantiating the model internally.
        """
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.dict(exclude_unset=True)
        db_object = self.model.model_validate(obj_in_data)   
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        
        return db_object


    def update(self, db: Session, db_obj: ModelType, obj_in: CreateUpdateSchemaType ) -> ModelType:
        """
        Update an existing database object with new values from a schema or dict.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
            
        for key, value in update_data.items(): 
            setattr(db_obj, key, value)
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    
    def delete(self, db: Session, db_obj: ModelType) -> None:
        """Delete an existing database object."""
        db.delete(db_obj)
        db.commit()