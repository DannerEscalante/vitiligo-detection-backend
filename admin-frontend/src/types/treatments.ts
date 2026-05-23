export interface TreatmentTypeAdmin {
  id: number;
  nombre: string;
  descripcion: string | null;
  total_usos: number;
  activos: number;
  continuaciones: number;
  pacientes_unicos: number;
  doctores_unicos: number;
}

export interface TreatmentTypeTopDoctor {
  doctor_id: number;
  nombre: string;
  usos: number;
}

export interface TreatmentTypeRecentUse {
  id: number;
  paciente_nombre: string;
  doctor_nombre: string;
  estado: string;
  fecha_inicio: string | null;
  fecha_fin: string | null;
}

export interface TreatmentTypeStats {
  datos_basicos: {
    id: number;
    nombre: string;
    descripcion: string | null;
  };
  total_usos: number;
  activos: number;
  finalizados: number;
  continuaciones: number;
  pacientes_unicos: number;
  doctores_unicos: number;
  top_doctores: TreatmentTypeTopDoctor[];
  pacientes_relacionados: Array<{
    paciente_id: number;
    nombre: string;
    usos: number;
  }>;
  doctores_relacionados: TreatmentTypeTopDoctor[];
  ultimos_usos: TreatmentTypeRecentUse[];
}

export interface TreatmentTypeCreatePayload {
  nombre: string;
  descripcion?: string;
}

export interface TreatmentTypeUpdatePayload {
  nombre?: string;
  descripcion?: string;
}

export interface TreatmentTypeMutationResult {
  mensaje?: string;
  id: number;
  nombre: string;
  descripcion: string | null;
}
