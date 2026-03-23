from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.security import hash_password, get_current_user
from app.models.user import User, UserRoleEnum
from app.schemas.user import UserRead, UserCreate

router = APIRouter(prefix="/users", tags=["users"])


# Create User (Admin only)
@router.post("/", response_model=UserRead)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 🔒 Access control
    if current_user.role != UserRoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create users"
        )

    # 🔍 Check duplicate email
    result = await db.execute(
        select(User).where(User.email == user.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # ✅ Create user
    new_user = User(
        tenant_id=current_user.tenant_id,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


# Get all users for tenant
@router.get("/", response_model=list[UserRead])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = await db.execute(
        select(User).where(User.tenant_id == current_user.tenant_id)
    )

    users = result.scalars().all()

    return users