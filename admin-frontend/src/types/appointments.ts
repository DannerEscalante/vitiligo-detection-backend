export type AppointmentStatus = "pendiente" | "confirmada" | "finalizada" | "cancelada";

export type AppointmentStatusFilter = AppointmentStatus | "todas";

export interface PatientSummary {
  id: number;
  nombre: string;
  fecha_nacimiento?: string | null;
  sexo?: string | null;
}

export interface DoctorSummary {
  id: number;
  nombre: string;
}

export interface PredictionSummary {
  id: number;
  resultado: string;
  confianza: number;
  imagen: string | null;
}

export interface Appointment {
  id: number;
  fecha_hora: string;
  estado: AppointmentStatus;
  duracion: number;
  paciente: PatientSummary | null;
  doctor: DoctorSummary | null;
  prediccion: PredictionSummary | null;
}
