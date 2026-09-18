import os
from datetime import datetime, timedelta
<<<<<<< HEAD
from typing import List, Tuple
from fastapi import Depends, HTTPException, status, Header
=======
from fastapi import Cookie, Depends, HTTPException, status
>>>>>>> a583192508a8de8f5f8a80617669f41a01d080f0
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from . import repository, schemas
from .audit_service import registrar_accion
from .models import UsuarioFincaRol, Organizacion, Finca, RolEnum

# ============================================================
# CONFIGURACIÓN
# ============================================================
SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "cambia-esta-clave-en-.env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def crear_token(usuario_id: int, organizacion_id: int) -> str:
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(usuario_id), "org_id": organizacion_id, "exp": expira}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def registrar_usuario(db: Session, datos: schemas.UsuarioCreate, ip_address: str = None):
    if repository.get_usuario_by_email(db, datos.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    org_id = datos.organizacion_id
    rol_org = RolEnum.operario

    # Si no hay org_id, creamos una nueva organización (Autoregistro)
    if not org_id:
        nombre_org = datos.nombre_organizacion or f"Ganadería de {datos.email.split('@')[0]}"
        nueva_org = Organizacion(nombre=nombre_org)
        db.add(nueva_org)
        db.commit()
        db.refresh(nueva_org)
        org_id = nueva_org.id
        rol_org = RolEnum.admin

        # Crear finca inicial por defecto
        finca_inicial = Finca(nombre="Mi Finca Principal", organizacion_id=org_id)
        db.add(finca_inicial)
        db.commit()
        db.refresh(finca_inicial)

    password_hash = hash_password(datos.password)
    usuario = repository.crear_usuario(db, datos.email, password_hash, org_id, rol_organizacion=rol_org)
    
    # Si es autoregistro, darle rol de admin en la finca inicial
    if not datos.organizacion_id:
        finca = db.query(Finca).filter(Finca.organizacion_id == org_id).first()
        if finca:
            rol_vinculo = UsuarioFincaRol(usuario_id=usuario.id, finca_id=finca.id, rol=RolEnum.admin)
            db.add(rol_vinculo)
            db.commit()
            db.refresh(usuario) # Recargar para incluir la relación finca_roles

    registrar_accion(db, "REGISTRO_USUARIO", usuario.id, usuario.email, f"OrgID: {org_id}", ip_address, organizacion_id=org_id)

    # Retornar una estructura plana para evitar errores de relación en el primer registro
    return {
        "id": usuario.id,
        "email": usuario.email,
        "organizacion_id": usuario.organizacion_id,
        "fincas_autorizadas": [],
        "created_at": usuario.created_at
    }

def autenticar_usuario(db: Session, datos: schemas.UsuarioLogin, ip_address: str = None):
    print(f"DEBUG LOGIN: Intentando entrar con email: '{datos.email}'")
    usuario = repository.get_usuario_by_email(db, datos.email)
    if not usuario or not verificar_password(datos.password, usuario.password_hash):
        registrar_accion(db, "LOGIN_FALLIDO", email=datos.email, detalles="Credenciales incorrectas", ip=ip_address)
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    token = crear_token(usuario.id, usuario.organizacion_id)

    # Obtener fincas autorizadas y roles contextuales
    fincas_autorizadas = []
    for fr in usuario.finca_roles:
        fincas_autorizadas.append({
            "id": fr.finca.id,
            "nombre": fr.finca.nombre,
            "rol": fr.rol.value if hasattr(fr.rol, "value") else str(fr.rol)
        })

    usuario_data = {
        "id": usuario.id,
        "email": usuario.email,
        "organizacion_id": usuario.organizacion_id,
        "fincas_autorizadas": fincas_autorizadas,
        "created_at": usuario.created_at
    }

    registrar_accion(db, "LOGIN_EXITOSO", usuario.id, usuario.email, ip=ip_address, organizacion_id=usuario.organizacion_id)
    return token, usuario_data

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

def get_finca_actual(
    x_finca_id: int = Header(None, alias="X-Finca-ID"),
    usuario=Depends(get_usuario_actual),
    db: Session = Depends(get_db)
):
    if not x_finca_id:
        raise HTTPException(status_code=400, detail="Se requiere X-Finca-ID header")

    permiso = db.query(UsuarioFincaRol).filter(
        UsuarioFincaRol.usuario_id == usuario.id,
        UsuarioFincaRol.finca_id == x_finca_id
    ).first()

    if not permiso:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta finca")

    return x_finca_id, permiso.rol

def requerir_rol_organizacion(*roles_permitidos: str):
    def verificador(usuario=Depends(get_usuario_actual)):
        rol_usuario = usuario.rol_organizacion.value if hasattr(usuario.rol_organizacion, "value") else str(usuario.rol_organizacion)
        if rol_usuario not in roles_permitidos:
            raise HTTPException(status_code=403, detail="Sin permisos administrativos en la organización")
        return usuario
    return verificador

def requerir_rol(*roles_permitidos: str):
    def verificador(contexto: Tuple[int, str] = Depends(get_finca_actual)):
        finca_id, rol_usuario = contexto
        rol_str = rol_usuario.value if hasattr(rol_usuario, "value") else str(rol_usuario)
        if rol_str not in roles_permitidos:
            raise HTTPException(status_code=403, detail=f"Sin permisos para esta finca (Rol: {rol_str})")
        return finca_id, rol_str # Devolvemos ambos para mayor utilidad en el router
    return verificador

def obtener_logs_auditoria(db: Session):
    return repository.get_logs_auditoria(db)

def provisionar_nueva_cuenta(db: Session, data: schemas.ProvisionRequest):
    # 1. Verificar si el usuario ya existe
    if repository.get_usuario_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="El correo ya está registrado en GAVAC")

    try:
        # 2. Crear Organización
        nueva_org = Organizacion(
            nombre=data.nombre_organizacion,
            nit=data.nit
        )
        db.add(nueva_org)
        db.commit()
        db.refresh(nueva_org)

        # 3. Crear Usuario (Propietario)
        password_hash_val = hash_password(data.password)
        # El primer usuario de una org siempre es admin en la org
        nuevo_usuario = repository.crear_usuario(
            db,
            email=data.email,
            password_hash=password_hash_val,
            organizacion_id=nueva_org.id,
            rol_organizacion=RolEnum.admin
        )

        # 4. Crear Finca Inicial
        finca_inicial = Finca(
            nombre="Finca Principal",
            organizacion_id=nueva_org.id
        )
        db.add(finca_inicial)
        db.commit()
        db.refresh(finca_inicial)

        # 5. Asignar rol de admin en la finca inicial
        rol_finca = UsuarioFincaRol(
            usuario_id=nuevo_usuario.id,
            finca_id=finca_inicial.id,
            rol=RolEnum.admin
        )
        db.add(rol_finca)

        db.commit()

        registrar_accion(db, "PROVISION_SAAS_EXITOSA", nuevo_usuario.id, nuevo_usuario.email, f"Nueva Org: {nueva_org.nombre}", organizacion_id=nueva_org.id)

        return {
            "status": "success",
            "usuario_id": nuevo_usuario.id,
            "organizacion_id": nueva_org.id,
            "finca_id": finca_inicial.id,
            "mensaje": "Cuenta provisionada correctamente"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en la provisión: {str(e)}")
