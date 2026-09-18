from typing import List
from fastapi import APIRouter, Depends, Request, Header, HTTPException
from sqlalchemy.orm import Session
import os

from app.database import get_db

from . import schemas, service

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post("/register", response_model=schemas.UsuarioOut, status_code=201)
def register(datos: schemas.UsuarioCreate, request: Request, db: Session = Depends(get_db)):
    return service.registrar_usuario(db, datos, request.client.host)


@router.post("/login", response_model=schemas.Token)
def login(datos: schemas.UsuarioLogin, request: Request, db: Session = Depends(get_db)):
    token, usuario = service.autenticar_usuario(db, datos, request.client.host)
    return schemas.Token(access_token=token, usuario=usuario)


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

@router.post("/provision", response_model=schemas.ProvisionResponse)
def provisionar_cuenta(
    data: schemas.ProvisionRequest,
    db: Session = Depends(get_db),
    x_api_key: str = Header(None, alias="X-GAVAC-Provision-Key")
):
    """
    Endpoint especial para la Landing Page.
    Crea una nueva organización y un usuario administrador.
    """
    secret_key = os.getenv("GAVAC_PROVISION_KEY")
    if not secret_key or x_api_key != secret_key:
        raise HTTPException(status_code=401, detail="API Key de provisión inválida o ausente")

    return service.provisionar_nueva_cuenta(db, data)
