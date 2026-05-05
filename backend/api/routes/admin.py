import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db import get_db
from models.user import User
from core.security import hash_password
from api.schemas.class_schema import UserCreate, UserResponse
from api.deps import get_current_user, require_role

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Roles a teacher is allowed to create
_TEACHER_CREATABLE = {"student"}
# All roles an admin can create
_ADMIN_CREATABLE = {"student", "teacher", "admin"}


@router.get("/users/", response_model=list[UserResponse])
async def list_users(
    role: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("teacher", "admin")),
):
    q = select(User)
    if current_user.role == "teacher":
        q = q.where(User.role == "student")
    elif role:
        q = q.where(User.role == role)
    q = q.order_by(User.last_name, User.first_name)
    result = await db.execute(q)
    return result.scalars().all()


@router.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("teacher", "admin")),
):
    allowed = _TEACHER_CREATABLE if current_user.role == "teacher" else _ADMIN_CREATABLE
    if data.role not in allowed:
        raise HTTPException(status_code=403, detail=f"Vous ne pouvez pas créer un compte de rôle '{data.role}'")

    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Un compte avec cet e-mail existe déjà")

    user = User(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        role=data.role,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas supprimer votre propre compte")
    await db.delete(user)
    await db.commit()
