import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from models import Rol, Usuario, Doctor

db = SessionLocal()
try:
    print("--- ROLES ---")
    roles = db.query(Rol).all()
    for r in roles:
        print(f"ID: {r.id}, Nombre: '{r.nombre_rol}'")
    
    print("\n--- DOCTORES ---")
    doctores = db.query(Doctor).all()
    print(f"Total doctores: {len(doctores)}")
    for d in doctores:
        print(f"ID: {d.id}, Nombre: {d.nombre}, UsuarioID: {d.usuario_id}, Sexo: {d.sexo}, FechaNac: {d.fecha_nacimiento}")

    print("\n--- USUARIOS CON ROL DOCTOR/ADMIN/GERENTE ---")
    usuarios = db.query(Usuario).all()
    for u in usuarios:
        rol_name = u.rol.nombre_rol if u.rol else "Sin Rol"
        if rol_name.strip().lower() in ["admin", "gerente", "doctor", "médico", "medico"]:
            print(f"Usuario ID: {u.id}, Email: {u.email}, Rol: '{rol_name}'")

finally:
    db.close()
