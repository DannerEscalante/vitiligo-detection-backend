export interface DoctorAdminSummary {
  id: number;
  nombre: string;
  sexo: string | null;
  fecha_nacimiento: string | null;
  edad: number | null;
  citas_pendientes: number;
  citas_confirmadas: number;
  citas_canceladas: number;
  disponibilidad: "alta" | "media" | "alta carga";
}

export interface DoctorBasicData {
  id: number;
  nombre: string;
  sexo: string | null;
  fecha_nacimiento: string | null;
  email: string | null;
}

export interface DoctorAppliedTreatment {
  id: number;
  paciente_nombre: string;
  tipo_tratamiento: string;
  fecha_inicio: string | null;
  estado: string;
  notas: string | null;
}

export interface DoctorStats {
  datos_basicos: DoctorBasicData;
  total_citas: number;
  pacientes_unicos: number;
  distribucion_estados: {
    pendiente: number;
    confirmada: number;
    cancelada: number;
    finalizada: number;
  };
  tratamientos_aplicados: DoctorAppliedTreatment[];
}

export interface DoctorRecentAppointment {
  id: number;
  fecha_hora: string | null;
  estado: string;
  paciente_nombre: string;
}

export interface DoctorRecentHistory {
  id: number;
  fecha: string | null;
  paciente_nombre: string;
  diagnostico: string;
}

export interface DoctorRecentPatient {
  id: number;
  nombre: string;
  sexo: string | null;
  fecha_nacimiento: string | null;
  edad: number | null;
}

export interface DoctorRecentActivity {
  ultimas_citas: DoctorRecentAppointment[];
  ultimos_historiales: DoctorRecentHistory[];
  ultimos_pacientes: DoctorRecentPatient[];
}

export interface DoctorRegistrationPayload {
  nombre: string;
  sexo: string;
  fecha_nacimiento: string;
  email: string;
  contrasena_temporal?: string;
}

export interface DoctorRegistrationResult {
  mensaje: string;
  doctor_id: number;
  email: string;
  contrasena_temporal: string;
}
