from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.auth_models import RolEnum, Usuario
from app.services.auth_service import get_usuario_actual

from app.schemas.empleados_schemas import EmpleadoOut

router = APIRouter(prefix="/api/empleados", tags=["Empleados"])


def require_admin(usuario=Depends(get_usuario_actual)):
    rol = usuario.rol.value if isinstance(usuario.rol, RolEnum) else str(usuario.rol)
    if rol != RolEnum.admin.value:
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")
    return usuario


@router.get("/", response_model=list[EmpleadoOut])
def listar_empleados(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    return db.query(Usuario).order_by(Usuario.created_at.desc()).all()
