export interface AdminPatient {
  id: number;
  nombre: string;
  sexo: string | null;
  fecha_nacimiento: string | null;
}

export interface ActiveTreatment {
  tiene_tratamiento: boolean;
  tratamiento_id: number | null;
  tipo_tratamiento: string | null;
  fecha_inicio: string | null;
  estado: string | null;
  notas: string | null;
}

export interface ClinicalPrediction {
  resultado: string;
  confianza: number;
  imagen: string | null;
  fecha: string | null;
}

export interface ClinicalTreatment {
  id: number;
  tipo_tratamiento?: string | null;
  estado: string;
  fecha_inicio: string | null;
  fecha_fin: string | null;
  notas: string | null;
  predicciones: ClinicalPrediction[];
}

export interface ClinicalHistory {
  id: number;
  fecha: string;
  diagnostico: string;
  tratamientos: ClinicalTreatment[];
}

export interface PatientWithTreatment extends AdminPatient {
  tratamiento_activo?: ActiveTreatment;
}
