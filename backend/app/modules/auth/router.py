from typing import List
import os
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.database import get_db

from . import schemas, service

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post("/register", response_model=schemas.UsuarioOut, status_code=201)
def register(datos: schemas.UsuarioCreate, request: Request, db: Session = Depends(get_db)):
    return service.registrar_usuario(db, datos, request.client.host)


@router.post("/login", response_model=schemas.Token)
def login(datos: schemas.UsuarioLogin, request: Request, response: Response, db: Session = Depends(get_db)):
    token, usuario = service.autenticar_usuario(db, datos, request.client.host)
    response.set_cookie(
        key="session_token",
        value=token,
        max_age=service.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        samesite="lax",
    )
    return schemas.Token(access_token=token, usuario=usuario)


@router.post("/logout", status_code=204)
def logout(response: Response):
    response.delete_cookie("session_token")


@router.get("/me", response_model=schemas.UsuarioOut)
def me(usuario_actual=Depends(service.get_usuario_actual)):
    return usuario_actual


@router.get("/auditoria", response_model=List[schemas.AuditoriaLogOut])
def ver_auditoria(
    db: Session = Depends(get_db),
    usuario=Depends(service.requerir_rol("admin"))
):
    """
    Lista los últimos logs de auditoría. Solo accesible por administradores.
    """
    return service.obtener_logs_auditoria(db)


@router.get("/solo-admin")
def solo_admin(usuario=Depends(service.requerir_rol("admin"))):
    return {"mensaje": f"Bienvenido admin {usuario.email}"}