from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from app.core.logger import get_logger

from app.core.database import get_db
from app.core.security import hash_password, get_current_user, verify_password, create_access_token
from app.models.user import User
from app.models.company import Company
from app.schemas.user import UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


# Register Company + Admin
@router.post("/register-company", response_model=UserRead)
async def register_company(
    company_name: str,
    email: str,
    password: str,
    db: AsyncSession = Depends(get_db)
):

    # check if email exists
    result = await db.execute(
        select(User).where(User.email == email)
    )
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # create company
    company = Company(name=company_name)

    db.add(company)
    await db.commit()
    await db.refresh(company)

    # create admin user
    user = User(
        tenant_id=company.id,
        email=email,
        hashed_password=hash_password(password),
        role="admin"
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    access_token = create_access_token(
        subject=str(user.id),
        tenant_id=str(company.id),
        role=user.role
    )

    return user


# Login
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User).where(User.email == form_data.username)
    )

    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User disabled"
        )

    token = create_access_token(
        subject=str(user.id),
        tenant_id=str(user.tenant_id),
        role=user.role
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
logger = get_logger("auth")