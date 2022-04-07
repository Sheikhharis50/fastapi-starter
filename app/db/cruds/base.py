from sqlalchemy.orm import Session
from typing import Any, Dict


class BaseCrud(object):
    page_size = 10

    def __init__(self) -> None:
        assert hasattr(
            self, "schema"
        ), "`schema` field must be provided in every crud class"

    def __init__(self, db: Session) -> None:
        self.db = db
        super().__init__()

    def get(self, skip: int = 0, limit: int | None = None):
        return (
            self.db.query(self.schema)
            .offset(skip)
            .limit(limit if limit else self.page_size)
            .all()
        )

    def create(self, obj: Dict[str, Any]):
        instance = self.schema(**(obj if isinstance(obj, dict) else obj.dict()))
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get_object(self, pk: str):
        return self.db.query(self.schema).filter(self.schema.id == pk).first()

    def update(self, pk: str, obj: Dict[str, Any]):
        instance = self.get_object(self.db, pk).update(
            **(obj if isinstance(obj, dict) else obj.dict())
        )
        self.db.commit()
        return instance

    def delete(self, pk: str):
        self.get_object(self.db, pk).delete()
        self.db.commit()
