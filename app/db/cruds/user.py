from passlib.context import CryptContext

from .base import BaseCrud
from ..schemas import User
from app.models import (
    UserCreate,
    AuthLogin,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCrud(BaseCrud):
    schema = User

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create(self, user: UserCreate):
        user.password = self._get_password_hash(user.password)
        return super().create(user.dict(exclude={"confirm_password"}))

    def get_object_email(self, email: str):
        return self.db.query(self.schema).filter(self.schema.email == email).first()

    def authenticate(self, user: AuthLogin):
        instance = self.get_object_email(user.email)
        if instance and self._verify_password(user.password, instance.password):
            return instance
        return None
