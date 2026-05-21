import { getApiUrl } from "@/lib/api";
import { getStoredAccessToken } from "@/lib/auth-token";
import type {
  MostContinuedTreatmentReport,
  MostUsedTreatmentReport
} from "@/types/reports";

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

export async function getMostUsedTreatments() {
  const response = await fetch(getApiUrl("/reportes/tratamientos-mas-usados/"), {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<MostUsedTreatmentReport[]>;
}

export async function getMostContinuedTreatments() {
  const response = await fetch(getApiUrl("/reportes/tratamientos-mas-continuados/"), {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<MostContinuedTreatmentReport[]>;
}
