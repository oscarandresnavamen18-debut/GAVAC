from getpass import getpass

from app.database import SessionLocal
from app.modules.auth import repository, service
from app.modules.auth.models import RolEnum


def main() -> None:
    email = input("Correo del administrador: ").strip()
    password = getpass("Contraseña del administrador: ")
    confirmation = getpass("Confirmar contraseña: ")

    if not email or not password:
        raise SystemExit("El correo y la contraseña son obligatorios.")
    if password != confirmation:
        raise SystemExit("Las contraseñas no coinciden.")
    if repository.get_usuario_by_email(db := SessionLocal(), email):
        db.close()
        raise SystemExit("Ese correo ya está registrado.")

    try:
        user = repository.crear_usuario(
            db,
            email,
            service.hash_password(password),
            RolEnum.admin,
        )
        print(f"Administrador creado con ID {user.id}.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
