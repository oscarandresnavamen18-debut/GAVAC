import os
from datetime import datetime, timedelta
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from . import repository, schemas
from .audit_service import registrar_accion

# ============================================================
# CONFIGURACIÓN
# ============================================================
SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "cambia-esta-clave-en-.env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def crear_token(usuario_id: int, rol: str) -> str:
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(usuario_id), "rol": rol, "exp": expira}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def registrar_usuario(db: Session, datos: schemas.UsuarioCreate, ip_address: str = None):
    if datos.rol == schemas.RolEnum.admin:
        raise HTTPException(status_code=403, detail="El rol administrador debe ser asignado por otro administrador")

    if repository.get_usuario_by_email(db, datos.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    password_hash = hash_password(datos.password)
    usuario = repository.crear_usuario(db, datos.email, password_hash, datos.rol)
    
    registrar_accion(db, "REGISTRO_USUARIO", usuario.id, usuario.email, f"Rol: {datos.rol}", ip_address)
    return usuario

def autenticar_usuario(db: Session, datos: schemas.UsuarioLogin, ip_address: str = None):
    usuario = repository.get_usuario_by_email(db, datos.email)
    if not usuario or not verificar_password(datos.password, usuario.password_hash):
        registrar_accion(db, "LOGIN_FALLIDO", email=datos.email, detalles="Credenciales incorrectas", ip=ip_address)
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    rol_str = usuario.rol.value if hasattr(usuario.rol, "value") else str(usuario.rol)
    token = crear_token(usuario.id, rol_str)
    registrar_accion(db, "LOGIN_EXITOSO", usuario.id, usuario.email, ip=ip_address)
    return token, usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def get_usuario_actual(
    token: str | None = Depends(oauth2_scheme),
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    token = token or session_token
    if not token:
        raise HTTPException(status_code=401, detail="Autenticación requerida", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = int(payload.get("sub"))
        usuario = repository.get_usuario_by_id(db, usuario_id)
        if not usuario: raise Exception()
        return usuario
    except:
        raise HTTPException(status_code=401, detail="Token inválido", headers={"WWW-Authenticate": "Bearer"})

def requerir_rol(*roles_permitidos: str):
    def verificador(usuario=Depends(get_usuario_actual)):
        rol_usuario = usuario.rol.value if hasattr(usuario.rol, "value") else str(usuario.rol)
        if rol_usuario not in roles_permitidos:
            raise HTTPException(status_code=403, detail="Sin permisos")
        return usuario
    return verificador

def obtener_logs_auditoria(db: Session):
    return repository.get_logs_auditoria(db)
