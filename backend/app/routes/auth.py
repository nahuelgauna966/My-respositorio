from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import LoginRequest, TokenResponse, UsuarioCreate, UsuarioResponse
from app.services.auth_service import (
    crear_usuario,
    create_access_token,
    get_current_user,
    get_usuario_by_email,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    # 1. Buscar el usuario por email
    usuario = await get_usuario_by_email(db, data.email)

    # 2. Verificar que existe y que la contraseña es correcta
    if not usuario or not verify_password(data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )

    # 3. Generar el token JWT
    token = create_access_token({"sub": str(usuario.id), "rol": usuario.rol})

    return TokenResponse(access_token=token, usuario=usuario)


@router.post("/register", response_model=UsuarioResponse, status_code=201)
async def register(data: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    # Verificar que el email no esté en uso
    existente = await get_usuario_by_email(db, data.email)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado",
        )
    usuario = await crear_usuario(db, data)
    return usuario


@router.get("/me", response_model=UsuarioResponse)
async def get_me(current_user: Usuario = Depends(get_current_user)):
    return current_user