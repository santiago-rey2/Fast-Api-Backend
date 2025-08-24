"""
Rutas de autenticación
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.auth.service import AuthService
from src.auth.dependencies import get_current_active_user, get_current_admin_user
from src.schemas.auth import (
    Token, LoginRequest, UserCreate, UserOut, UserUpdate, UserInToken
)
from src.entities.user import User
from src.core.config import settings

router = APIRouter(
    prefix="/auth", 
    tags=["🔐 Autenticación y Usuarios"],
    responses={
        401: {"description": "No autorizado"},
        403: {"description": "Permisos insuficientes"}
    }
)

@router.post(
    "/login", 
    response_model=Token,
    summary="🔑 Iniciar sesión",
    description="Autentica un usuario con username y password, devuelve un token JWT para acceso a endpoints protegidos.",
    response_description="Token de acceso JWT"
)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Iniciar sesión con username y password
    """
    user = AuthService.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = AuthService.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserOut)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registrar nuevo usuario (público para el primer admin)
    """
    # Verificar si es el primer usuario (será admin automáticamente)
    user_count = db.query(User).count()
    is_first_user = user_count == 0
    
    user = AuthService.create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        is_admin=is_first_user or user_data.is_admin
    )
    
    return user

@router.get("/me", response_model=UserInToken)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener información del usuario actual
    """
    return current_user

@router.put("/me", response_model=UserOut)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar información del usuario actual
    """
    # Actualizar campos permitidos
    if user_update.username is not None:
        # Verificar que el nuevo username no exista
        existing_user = AuthService.get_user_by_username(db, user_update.username)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El username ya existe"
            )
        current_user.username = user_update.username
    
    if user_update.email is not None:
        # Verificar que el nuevo email no exista
        existing_user = AuthService.get_user_by_email(db, user_update.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        current_user.email = user_update.email
    
    if user_update.password is not None:
        current_user.hashed_password = AuthService.get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    return current_user

# ==================== RUTAS DE ADMINISTRACIÓN DE USUARIOS ====================

@router.get("/users", response_model=List[UserOut])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de usuarios (solo administradores)
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("/users", response_model=UserOut)
async def create_user_admin(
    user_data: UserCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Crear usuario (solo administradores)
    """
    user = AuthService.create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        is_admin=user_data.is_admin
    )
    return user

@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Obtener usuario por ID (solo administradores)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user

@router.put("/users/{user_id}", response_model=UserOut)
async def update_user_admin(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar usuario (solo administradores)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Actualizar campos
    if user_update.username is not None:
        existing_user = AuthService.get_user_by_username(db, user_update.username)
        if existing_user and existing_user.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El username ya existe"
            )
        user.username = user_update.username
    
    if user_update.email is not None:
        existing_user = AuthService.get_user_by_email(db, user_update.email)
        if existing_user and existing_user.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        user.email = user_update.email
    
    if user_update.password is not None:
        user.hashed_password = AuthService.get_password_hash(user_update.password)
    
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    
    if user_update.is_admin is not None:
        user.is_admin = user_update.is_admin
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar usuario (solo administradores)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # No permitir que se elimine a sí mismo
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propia cuenta"
        )
    
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}
