from typing import TypeVar, Type, Generic, Optional, List, Any
from fastapi import HTTPException
from sqlmodel import Session, select
from uuid import UUID

ModelType = TypeVar("ModelType", bound=Any)

class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

   
    def get_single(self, db: Session, id: UUID) -> Optional[ModelType]:
        statement = select(self.model).where(self.model.id == id)
        result = db.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        return result

    def get_all(self, db: Session, skip: int = 0, limit: int = 10) -> List[ModelType]:
        statement = select(self.model).offset(skip).limit(limit)
        return list(db.exec(statement).all())

    def get_by_user(
        self, db: Session, user_id: UUID, skip: int = 0, limit: int = 10
    ) -> List[ModelType]:
        if not hasattr(self.model, "owner_id"):
            raise HTTPException(
                status_code=400,
                detail=f"{self.model.__name__} does not have an 'owner_id' field.",
            )
        statement = (
            select(self.model)
            .where(self.model.owner_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return list(db.exec(statement).all())

    def create(self, db: Session, obj_in: ModelType) -> ModelType:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def update(self, db: Session , obj_in: dict[str, Any],db_obj: ModelType) -> ModelType:
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: ModelType) -> None:
        db.delete(db_obj)
        db.commit()
