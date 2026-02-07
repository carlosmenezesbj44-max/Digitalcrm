from typing import Generic, TypeVar, List, Optional
from sqlalchemy.orm import Session
from crm_core.db.models_base import Base

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: T):
        self.session = session
        self.model = model

    def get_by_id(self, id: int) -> Optional[T]:
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[T]:
        return self.session.query(self.model).all()

    def create(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, obj: T) -> T:
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj: T) -> None:
        self.session.delete(obj)
        self.session.commit()
