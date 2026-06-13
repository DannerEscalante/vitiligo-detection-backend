from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
import random
import string

from core.database import SessionLocal
from core.deps import obtener_usuario_actual, requerir_admin_o_gerente

from models import Doctor, Usuario
from models.rol import Rol
from models.cita import Cita
from models.historial_clinico import HistorialClinico
from models.tratamiento import Tratamiento
from core.security import verify_password, hash_password
router = APIRouter(prefix="/doctores", tags=["Doctores"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# LISTAR DOCTORES PARA ADMIN
# -------------------------------
@router.get("/")
def listar_doctores(
    usuario: Usuario = Depends(requerir_admin_o_gerente),
    db: Session = Depends(get_db)
):
    # Respuesta minima para dropdowns administrativos.
    doctores = db.query(Doctor).order_by(
        Doctor.nombre.asc()
    ).all()

    return [
        {
            "id": doctor.id,
            "nombre": doctor.nombre
        }
        for doctor in doctores
    ]


@router.post("/")
def crear_doctor(
    nombre: str,
    fecha_nacimiento: str,
    sexo: str,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.id == int(usuario_id)
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    existente = db.query(Doctor).filter(
        Doctor.usuario_id == usuario.id
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="El doctor ya existe"
        )

    doctor = Doctor(
        usuario_id=usuario.id,
        nombre=nombre,
        fecha_nacimiento=fecha_nacimiento,
        sexo=sexo
    )

    db.add(doctor)

    db.commit()
    db.refresh(doctor)

    return doctor

@router.get("/perfil")
def obtener_perfil_doctor(
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.usuario_id == int(usuario_id)
    ).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")

    return {
        "id": doctor.id,
        "nombre": doctor.nombre,
        "email": doctor.usuario.email,
        "fecha_nacimiento": doctor.fecha_nacimiento,
        "sexo": doctor.sexo
    }
    
@router.put("/perfil")
def actualizar_perfil_doctor(
    email: str = None,
    contrasena: str = None,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.usuario_id == int(usuario_id)
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor no encontrado"
        )

    usuario = db.query(Usuario).filter(
        Usuario.id == doctor.usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if email:

        existente = db.query(Usuario).filter(
            Usuario.email == email
        ).first()

        if existente and existente.id != usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El email ya está en uso"
            )

        usuario.email = email

    if contrasena:

        usuario.contrasena = hash_password(contrasena)

    db.commit()
    db.refresh(usuario)

    return {
        "mensaje": "Perfil actualizado correctamente"
    }
    
# -------------------------------
# PACIENTES DEL DOCTOR
# -------------------------------
@router.get("/doctor")
def obtener_pacientes_doctor(
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.usuario_id == int(usuario_id)
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=403,
            detail="Solo doctores"
        )

    historiales = db.query(HistorialClinico).filter(
        HistorialClinico.doctor_id == doctor.id
    ).all()

    pacientes_unicos = {}

    for h in historiales:

        paciente = h.paciente

        if paciente.id not in pacientes_unicos:

            tratamiento_activo = db.query(Tratamiento).filter(
                Tratamiento.paciente_id == paciente.id,
                Tratamiento.estado == "activo"
            ).first()

            pacientes_unicos[paciente.id] = {
                "id": paciente.id,
                "nombre": paciente.nombre,
                "sexo": paciente.sexo,
                "fecha_nacimiento": paciente.fecha_nacimiento,
                "tratamiento_activo": (
                    True if tratamiento_activo else False
                )
            }

    return list(pacientes_unicos.values())    


# -----------------------------------------------------------------------------
# SCHEMAS Y ENDPOINTS ADMINISTRATIVOS (EXCLUSIVOS PARA PANEL GERENCIAL / WEB)
# -----------------------------------------------------------------------------

class DoctorAdminCreate(BaseModel):
    nombre: str
    sexo: str
    fecha_nacimiento: str  # Formato YYYY-MM-DD
    email: EmailStr
    contrasena_temporal: str = Field(default=None, min_length=6, max_length=50)


@router.get("/admin")
def listar_doctores_admin(
    usuario: Usuario = Depends(requerir_admin_o_gerente),
    db: Session = Depends(get_db)
):
    doctores = db.query(Doctor).order_by(Doctor.nombre.asc()).all()
    resultado = []
    
    for doc in doctores:
        # Calcular edad
        edad = None
        if doc.fecha_nacimiento:
            hoy = date.today()
            fn = doc.fecha_nacimiento
            try:
                edad = hoy.year - fn.year - ((hoy.month, hoy.day) < (fn.month, fn.day))
            except Exception:
                pass

        # Cargar estadísticas de citas
        citas = doc.citas
        
        citas_pendientes = sum(1 for c in citas if c.estado == "pendiente")
        citas_confirmadas = sum(1 for c in citas if c.estado == "confirmada")
        citas_canceladas = sum(1 for c in citas if c.estado == "cancelada")
        
        # Reglas de disponibilidad:
        # Solo las citas confirmadas asignadas al doctor ocupan disponibilidad.
        # Las pendientes aun no tienen asignacion clinica efectiva.
        # 0-2 confirmadas -> alta
        # 3-5 confirmadas -> media
        # 6+ confirmadas -> alta carga
        if citas_confirmadas <= 2:
            disponibilidad = "alta"
        elif citas_confirmadas <= 5:
            disponibilidad = "media"
        else:
            disponibilidad = "alta carga"
            
        resultado.append({
            "id": doc.id,
            "nombre": doc.nombre,
            "sexo": doc.sexo,
            "fecha_nacimiento": doc.fecha_nacimiento.isoformat() if doc.fecha_nacimiento else None,
            "edad": edad,
            "citas_pendientes": citas_pendientes,
            "citas_confirmadas": citas_confirmadas,
            "citas_canceladas": citas_canceladas,
            "disponibilidad": disponibilidad
        })
        
    return resultado


@router.post("/admin")
def crear_doctor_admin(
    datos: DoctorAdminCreate,
    usuario_admin: Usuario = Depends(requerir_admin_o_gerente),
    db: Session = Depends(get_db)
):
    # Validar si el email ya existe
    existente = db.query(Usuario).filter(Usuario.email == datos.email).first()
    if existente:
        raise HTTPException(
            status_code=400,
            detail="El correo electrónico ya está registrado."
        )
        
    # Obtener el rol del doctor (fallando explícitamente si no existe)
    rol_doctor = db.query(Rol).filter(
        func.lower(Rol.nombre_rol).in_(["doctor", "médico", "medico"])
    ).first()
    
    if not rol_doctor:
        raise HTTPException(
            status_code=400,
            detail="Rol doctor no encontrado"
        )
        
    # Validar fecha_nacimiento
    try:
        fecha_nac_obj = datetime.strptime(datos.fecha_nacimiento, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Formato de fecha inválido. Debe ser YYYY-MM-DD."
        )
        
    # Determinar contraseña temporal
    contrasena_temp = datos.contrasena_temporal
    if not contrasena_temp:
        # Generar una aleatoria de 8 caracteres
        caracteres = string.ascii_letters + string.digits
        contrasena_temp = "Doc-" + "".join(random.choices(caracteres, k=6))
        
    # Crear el usuario
    nuevo_usuario = Usuario(
        email=datos.email,
        contrasena=hash_password(contrasena_temp),
        rol_id=rol_doctor.id
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    # Crear el perfil del doctor
    nuevo_doctor = Doctor(
        usuario_id=nuevo_usuario.id,
        nombre=datos.nombre,
        fecha_nacimiento=fecha_nac_obj,
        sexo=datos.sexo
    )
    
    db.add(nuevo_doctor)
    db.commit()
    db.refresh(nuevo_doctor)
    
    return {
        "mensaje": "Doctor registrado correctamente",
        "doctor_id": nuevo_doctor.id,
        "email": nuevo_usuario.email,
        "contrasena_temporal": contrasena_temp
    }


@router.get("/{doctor_id}/estadisticas")
def obtener_estadisticas_doctor(
    doctor_id: int,
    usuario: Usuario = Depends(requerir_admin_o_gerente),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
        
    # Citas totales y distribución de estados
    citas = doctor.citas
    total_citas = len(citas)
    
    distribucion = {
        "pendiente": 0,
        "confirmada": 0,
        "cancelada": 0,
        "finalizada": 0
    }
    
    for c in citas:
        if c.estado in distribucion:
            distribucion[c.estado] += 1
            
    # Pacientes únicos atendidos
    pacientes_citas = {c.paciente_id for c in citas if c.estado in ["confirmada", "finalizada"]}
    pacientes_historiales = {h.paciente_id for h in doctor.historiales}
    pacientes_unicos_ids = pacientes_citas.union(pacientes_historiales)
    pacientes_unicos = len(pacientes_unicos_ids)
    
    # Tratamientos aplicados por este doctor
    tratamientos = db.query(Tratamiento).filter(
        Tratamiento.doctor_id == doctor.id
    ).order_by(Tratamiento.fecha_inicio.desc()).all()
    
    tratamientos_formateados = []
    for t in tratamientos:
        tratamientos_formateados.append({
            "id": t.id,
            "paciente_nombre": t.paciente.nombre if t.paciente else "Paciente Desconocido",
            "tipo_tratamiento": t.tipo_tratamiento.nombre if t.tipo_tratamiento else "Otro",
            "fecha_inicio": t.fecha_inicio.isoformat() if t.fecha_inicio else None,
            "estado": t.estado,
            "notas": t.notas
        })
        
    return {
        "datos_basicos": {
            "id": doctor.id,
            "nombre": doctor.nombre,
            "sexo": doctor.sexo,
            "fecha_nacimiento": doctor.fecha_nacimiento.isoformat() if doctor.fecha_nacimiento else None,
            "email": doctor.usuario.email if doctor.usuario else None
        },
        "total_citas": total_citas,
        "pacientes_unicos": pacientes_unicos,
        "distribucion_estados": distribucion,
        "tratamientos_aplicados": tratamientos_formateados
    }


@router.get("/{doctor_id}/actividad")
def obtener_actividad_doctor(
    doctor_id: int,
    usuario: Usuario = Depends(requerir_admin_o_gerente),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
        
    # Últimas 5 citas asignadas
    ultimas_citas_db = db.query(Cita).filter(
        Cita.doctor_id == doctor.id
    ).order_by(Cita.fecha_hora.desc()).limit(5).all()
    
    ultimas_citas = []
    for c in ultimas_citas_db:
        ultimas_citas.append({
            "id": c.id,
            "fecha_hora": c.fecha_hora.isoformat() if c.fecha_hora else None,
            "estado": c.estado,
            "paciente_nombre": c.paciente.nombre if c.paciente else "Paciente Desconocido"
        })
        
    # Últimos 5 historiales clínicos relacionados
    ultimos_historiales_db = db.query(HistorialClinico).filter(
        HistorialClinico.doctor_id == doctor.id
    ).order_by(HistorialClinico.fecha.desc()).limit(5).all()
    
    ultimos_historiales = []
    for h in ultimos_historiales_db:
        ultimos_historiales.append({
            "id": h.id,
            "fecha": h.fecha.isoformat() if h.fecha else None,
            "paciente_nombre": h.paciente.nombre if h.paciente else "Paciente Desconocido",
            "diagnostico": h.diagnostico
        })
        
    # Últimos 5 pacientes únicos atendidos (de citas confirmadas/finalizadas)
    citas_recientes = db.query(Cita).filter(
        Cita.doctor_id == doctor.id,
        Cita.estado.in_(["confirmada", "finalizada"])
    ).order_by(Cita.fecha_hora.desc()).all()
    
    pacientes_vistos = set()
    ultimos_pacientes = []
    for c in citas_recientes:
        if c.paciente and c.paciente.id not in pacientes_vistos:
            pacientes_vistos.add(c.paciente.id)
            edad_p = None
            if c.paciente.fecha_nacimiento:
                hoy = date.today()
                fn = c.paciente.fecha_nacimiento
                try:
                    edad_p = hoy.year - fn.year - ((hoy.month, hoy.day) < (fn.month, fn.day))
                except Exception:
                    pass
            ultimos_pacientes.append({
                "id": c.paciente.id,
                "nombre": c.paciente.nombre,
                "sexo": c.paciente.sexo,
                "fecha_nacimiento": c.paciente.fecha_nacimiento.isoformat() if c.paciente.fecha_nacimiento else None,
                "edad": edad_p
            })
            if len(ultimos_pacientes) >= 5:
                break
                
    return {
        "ultimas_citas": ultimas_citas,
        "ultimos_historiales": ultimos_historiales,
        "ultimos_pacientes": ultimos_pacientes
    }
