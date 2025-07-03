from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.user as user_schemas
import app.crud.crud_user as crud_user
from app.db.session import get_db_session
from app.api.deps.current_user import get_current_user
from app.models.user import User
from app.core.security import verify_password

router = APIRouter()

@router.get("/me", response_model=user_schemas.UserRead, tags=["Utilizadores"])
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=user_schemas.UserRead, tags=["Utilizadores"])
async def update_current_user(
    *, db: AsyncSession = Depends(get_db_session), user_in: user_schemas.UserUpdate, current_user: User = Depends(get_current_user)
):
    return await crud_user.update_user(db=db, db_user=current_user, user_in=user_in)

@router.post("/me/password", status_code=status.HTTP_204_NO_CONTENT, tags=["Utilizadores"])
async def update_current_user_password(
    *, db: AsyncSession = Depends(get_db_session), password_data: user_schemas.UserPasswordUpdate, current_user: User = Depends(get_current_user)
):
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A senha atual está incorreta.")
    await crud_user.update_user(db=db, db_user=current_user, user_in={"password": password_data.new_password})
    return

@router.post("/", response_model=user_schemas.UserRead, status_code=status.HTTP_201_CREATED, tags=["Utilizadores"])
async def register_new_user(
    *, db: AsyncSession = Depends(get_db_session), user_in: user_schemas.UserCreate
):
    if await crud_user.get_user_by_email(db, email=user_in.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Um utilizador com este email já existe.")
    return await crud_user.create_user(db=db, user_in=user_in)
