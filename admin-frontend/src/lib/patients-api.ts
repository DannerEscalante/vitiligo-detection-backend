import { getApiUrl } from "@/lib/api";
import { getStoredAccessToken } from "@/lib/auth-token";
import type { ActiveTreatment, AdminPatient, ClinicalHistory } from "@/types/patients";

function getAuthHeaders() {
  const token = getStoredAccessToken();

  if (!token) {
    throw new Error("No hay token de autenticacion. Inicia sesion nuevamente.");
  }

  return {
    Authorization: `Bearer ${token}`
  };
}

async function parseApiError(response: Response) {
  try {
    const body = await response.json();
    return body.detail ?? `Error HTTP ${response.status}`;
  } catch {
    return `Error HTTP ${response.status}`;
  }
}

export async function getPatients() {
  const response = await fetch(getApiUrl("/pacientes/"), {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<AdminPatient[]>;
}

export async function getPatientClinicalHistory(patientId: number) {
  const response = await fetch(getApiUrl(`/historial-clinico/doctor/paciente/${patientId}/`), {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<ClinicalHistory[]>;
}

export async function getPatientActiveTreatment(patientId: number) {
  const response = await fetch(getApiUrl(`/tratamientos/activo/paciente/${patientId}/`), {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<ActiveTreatment>;
}
