import { getApiUrl } from "@/lib/api";
import { getStoredAccessToken } from "@/lib/auth-token";
import type {
  TreatmentTypeAdmin,
  TreatmentTypeCreatePayload,
  TreatmentTypeMutationResult,
  TreatmentTypeStats,
  TreatmentTypeUpdatePayload
} from "@/types/treatments";

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

export async function getTreatmentTypesAdmin() {
  const response = await fetch(getApiUrl("/tipos-tratamiento/admin"), {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<TreatmentTypeAdmin[]>;
}

export async function createTreatmentTypeAdmin(payload: TreatmentTypeCreatePayload) {
  const response = await fetch(getApiUrl("/tipos-tratamiento/admin"), {
    method: "POST",
    headers: {
      ...getAuthHeaders(),
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<TreatmentTypeMutationResult>;
}

export async function updateTreatmentType(id: number, payload: TreatmentTypeUpdatePayload) {
  const response = await fetch(getApiUrl(`/tipos-tratamiento/${id}`), {
    method: "PUT",
    headers: {
      ...getAuthHeaders(),
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<TreatmentTypeMutationResult>;
}

export async function getTreatmentTypeStats(id: number) {
  const response = await fetch(getApiUrl(`/tipos-tratamiento/${id}/estadisticas`), {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<TreatmentTypeStats>;
}
