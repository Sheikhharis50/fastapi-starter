from typing import Generator
from fastapi import Header, HTTPException

from app.db.session import SessionLocal


async def get_token_header(token: str = Header(...)):
    # Build Your login here...
    if token != "123":
        raise HTTPException(status_code=400, detail="Invalid Token")


# return same database session instance
# once every request.
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
