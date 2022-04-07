from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from app.config import TOKEN_EXPIRE_MINUTES
from app.dependencies import get_db
from app.core.security import create_access_token, get_current_user
from app.db.cruds.user import UserCrud
from app.models import (
    # base
    ResponseModel,
    # user
    UserList,
    UserCreate,
    UserView,
    # auth
    AuthLogin,
    AuthToken,
)

router = APIRouter(responses={400: {"detail": "Invalid Data."}})

fake_users_db = [{"username": "Haris"}, {"username": "Hashir"}]


async def login(user: AuthLogin, db: Session = Depends(get_db)):
    instance = UserCrud(db).authenticate(user)
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials.",
        )

    token_data = AuthToken(
        access_token=create_access_token(
            data={"sub": instance.email},
            expires_delta=timedelta(minutes=TOKEN_EXPIRE_MINUTES),
        ),
        token_type="bearer",
    )
    return token_data


@router.post("/token", response_model=AuthToken)
async def login_with_form(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return await login(
        user=AuthLogin(
            email=form_data.username,
            password=form_data.password,
        ),
        db=db,
    )


@router.post("/login", response_model=ResponseModel)
async def login_with_json(user: AuthLogin, db: Session = Depends(get_db)):
    token_data = await login(user=user, db=db)
    return {
        "detail": "Login Successfully.",
        "data": token_data,
    }


@router.post("/register", response_model=UserView)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    crud = UserCrud(db)
    if crud.get_object_email(user.email):
        raise HTTPException(status_code=400, detail="User already exists.")
    if user.password.lower() != user.confirm_password.lower():
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    return crud.create(user)


@router.get("/whoami", response_model=UserView)
async def whoami(c_user: UserView = Depends(get_current_user)):
    return c_user


@router.get(
    "/user",
    dependencies=[Depends(get_current_user)],
    response_model=List[UserList],
)
async def get_users(
    skip: int = 0, limit: int | None = None, db: Session = Depends(get_db)
):
    return UserCrud(db).get(skip, limit)


@router.get(
    "/user/{user_id}",
    dependencies=[Depends(get_current_user)],
    response_model=UserView,
)
async def get_user(user_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    user = UserCrud(db).get_object(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Not Found.")
    return user
