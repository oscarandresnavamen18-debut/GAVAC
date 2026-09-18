from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.modules.auth.service import get_usuario_actual, requerir_rol_organizacion, hash_password
from app.modules.auth.audit_service import registrar_accion
from app.modules.auth.models import Finca, Usuario, UsuarioFincaRol
from .schemas import FincaCreate, FincaOut, UsuarioFincaAssignment, UsuarioCreateAdmin, UsuarioUpdateAdmin

router = APIRouter(prefix="/api/admin", tags=["Administración"])

# --- GESTIÓN DE FINCAS ---

@router.post("/fincas/", response_model=FincaOut, status_code=status.HTTP_201_CREATED)
def crear_finca(
    data: FincaCreate,
    db: Session = Depends(get_db),
    admin = Depends(requerir_rol_organizacion("admin", "ganadero"))
):
    db_finca = Finca(**data.model_dump(), organizacion_id=admin.organizacion_id)
    db.add(db_finca)
    db.commit()
    db.refresh(db_finca)
    registrar_accion(db, "CREACION_FINCA", admin.id, admin.email, f"Creó finca {db_finca.nombre}", organizacion_id=admin.organizacion_id)
    return db_finca

@router.get("/fincas/", response_model=List[FincaOut])
def listar_fincas(
    db: Session = Depends(get_db),
    admin = Depends(requerir_rol_organizacion("admin", "ganadero"))
):
    return db.query(Finca).filter(Finca.organizacion_id == admin.organizacion_id).all()

# --- ASIGNACIÓN DE ROLES CONTEXTUALES (FINCAS) ---

@router.post("/fincas/asignar-rol/")
def asignar_rol_finca(
    data: UsuarioFincaAssignment,
    db: Session = Depends(get_db),
    admin = Depends(requerir_rol_organizacion("admin"))
):
    usuario = db.query(Usuario).filter(Usuario.id == data.usuario_id, Usuario.organizacion_id == admin.organizacion_id).first()
    finca = db.query(Finca).filter(Finca.id == data.finca_id, Finca.organizacion_id == admin.organizacion_id).first()
    
    if not usuario or not finca:
        raise HTTPException(status_code=404, detail="Usuario o Finca no encontrado en su organización")

    # Crear o actualizar rol contextual
    permiso = db.query(UsuarioFincaRol).filter(
        UsuarioFincaRol.usuario_id == data.usuario_id,
        UsuarioFincaRol.finca_id == data.finca_id
    ).first()

    if not permiso:
        permiso = UsuarioFincaRol(
            usuario_id=data.usuario_id,
            finca_id=data.finca_id,
            rol=data.rol
        )
        db.add(permiso)
    else:
        permiso.rol = data.rol

    db.commit()
    registrar_accion(db, "ASIGNACION_ROL_FINCA", admin.id, admin.email, f"Asignó rol {data.rol} a {usuario.email} en {finca.nombre}", organizacion_id=admin.organizacion_id)
    return {"mensaje": f"Usuario {usuario.email} asignado a {finca.nombre} como {data.rol}"}

# --- LISTAR USUARIOS DE LA ORGANIZACIÓN ---

@router.get("/usuarios/", response_model=List[dict])
def listar_usuarios(
    db: Session = Depends(get_db),
    admin = Depends(requerir_rol_organizacion("admin"))
):
    usuarios = db.query(Usuario).filter(Usuario.organizacion_id == admin.organizacion_id).all()
    resultado = []
    for u in usuarios:
        finca_roles = []
        for fr in u.finca_roles:
            finca_roles.append({
                "finca_id": fr.finca_id,
                "finca_nombre": fr.finca.nombre,
                "rol": fr.rol
            })
        resultado.append({
            "id": u.id,
            "email": u.email,
            "rol_organizacion": u.rol_organizacion,
            "finca_roles": finca_roles
        })
    return resultado

# --- GESTIÓN MAESTRA DE USUARIOS (ORGANIZACIÓN) ---

@router.post("/usuarios/", status_code=status.HTTP_201_CREATED)
def crear_usuario_admin(
    data: UsuarioCreateAdmin,
    db: Session = Depends(get_db),
    admin = Depends(requerir_rol_organizacion("admin"))
):
    existente = db.query(Usuario).filter(Usuario.email == data.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    nuevo_usuario = Usuario(
        email=data.email,
        password_hash=hash_password(data.password),
        rol_organizacion=data.rol, # Rol base en la org
        organizacion_id=admin.organizacion_id
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    registrar_accion(db, "CREACION_USUARIO_ADMIN", admin.id, admin.email, f"Creó usuario {data.email} con rol base {data.rol}", organizacion_id=admin.organizacion_id)

    return {"id": nuevo_usuario.id, "email": nuevo_usuario.email, "rol_organizacion": nuevo_usuario.rol_organizacion}

@router.put("/usuarios/{usuario_id}/")
def actualizar_usuario_admin(
    usuario_id: int,
    data: UsuarioUpdateAdmin,
    db: Session = Depends(get_db),
    admin = Depends(requerir_rol_organizacion("admin"))
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.organizacion_id == admin.organizacion_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en su organización")

    if data.email:
        usuario.email = data.email
    if data.rol:
        usuario.rol_organizacion = data.rol

    db.commit()
    registrar_accion(db, "ACTUALIZACION_USUARIO_ADMIN", admin.id, admin.email, f"Actualizó usuario ID: {usuario_id}", organizacion_id=admin.organizacion_id)
    return {"status": "ok", "mensaje": "Usuario actualizado"}

@router.delete("/usuarios/{usuario_id}/", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario_admin(
    usuario_id: int,
    db: Session = Depends(get_db),
    admin = Depends(requerir_rol_organizacion("admin"))
):
    if admin.id == usuario_id:
        raise HTTPException(status_code=400, detail="No puedes eliminarte a ti mismo")

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.organizacion_id == admin.organizacion_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en su organización")

    email_borrado = usuario.email
    db.delete(usuario)
    db.commit()

    registrar_accion(db, "ELIMINACION_USUARIO_ADMIN", admin.id, admin.email, f"Eliminó usuario: {email_borrado}", organizacion_id=admin.organizacion_id)
    return None
