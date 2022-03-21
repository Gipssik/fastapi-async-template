import logging
from typing import Generic, List, Optional, Type

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.elements import ClauseElement

from app.schemas import ModelType, CreateType, UpdateType, ErrorModel
from app.exceptions import ModelNotFoundException

logger = logging.getLogger(__name__)


class CRUDBase(Generic[ModelType, CreateType, UpdateType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    @property
    def model(self) -> Type[ModelType]:
        return self._model

    async def create(
        self, db: AsyncSession, obj_in: CreateType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        logger.debug(f"{self._model.__name__} successfully created")
        return db_obj

    async def get(self, db: AsyncSession, obj_id: int) -> ModelType:
        result = await db.get(self._model, obj_id)

        if not result:
            logger.error(f"{self._model.__name__} id={obj_id} not found")
            error = ErrorModel(class_name=self._model.__name__, value=obj_id)
            raise ModelNotFoundException(error)

        logger.debug(f"{self._model.__name__} id={obj_id} found")
        return result

    async def list(
        self,
        db: AsyncSession,
        clauses: Optional[List[ClauseElement]] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
    ) -> List[ModelType]:

        if clauses is None:
            clauses = []

        query = (
            select(self._model).where(and_(True, *clauses)).offset(offset).limit(limit)
        )
        results = await db.execute(query)

        logger.debug(f"List all {self._model.__name__} successful")
        return results.scalars().all()

    async def count(self, db: AsyncSession) -> int:
        results = await db.execute(select(func.count(self._model.id)))
        (result,) = results.one()
        return result

    async def update(
        self, db: AsyncSession, obj_in: UpdateType, obj_id: int
    ) -> ModelType:

        db_obj: ModelType = await self.get(db, obj_id)

        update_data = obj_in.dict(exclude_unset=True)
        for field in jsonable_encoder(db_obj):
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        logger.debug(f"{self._model.__name__} id={obj_id} successfully updated")
        return db_obj

    async def delete(self, db: AsyncSession, obj_id: int) -> None:
        db_obj = await self.get(db, obj_id)
        await db.delete(db_obj)
        await db.commit()
        logger.debug(f"{self._model.__name__} successfully deleted")
