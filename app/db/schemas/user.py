from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
)

from ..base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True, nullable=False)
    password = Column(String(256), nullable=False)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    description = Column(Text, nullable=True)
    is_admin = Column(Boolean, default=False)
