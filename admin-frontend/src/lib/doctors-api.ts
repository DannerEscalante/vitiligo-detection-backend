import { getApiUrl } from "@/lib/api";
import { getStoredAccessToken } from "@/lib/auth-token";
import type { DoctorSummary } from "@/types/appointments";
import type {
  DoctorAdminSummary,
  DoctorStats,
  DoctorRecentActivity,
  DoctorRegistrationPayload,
  DoctorRegistrationResult
} from "@/types/doctors";

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

export async function getDoctors() {
  const response = await fetch(getApiUrl("/doctores/"), {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<DoctorSummary[]>;
}

export async function getDoctorsAdmin() {
  const response = await fetch(getApiUrl("/doctores/admin"), {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<DoctorAdminSummary[]>;
}

export async function getDoctorStats(id: number) {
  const response = await fetch(getApiUrl(`/doctores/${id}/estadisticas`), {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<DoctorStats>;
}

export async function getDoctorActivity(id: number) {
  const response = await fetch(getApiUrl(`/doctores/${id}/actividad`), {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<DoctorRecentActivity>;
}

export async function createDoctorAdmin(payload: DoctorRegistrationPayload) {
  const response = await fetch(getApiUrl("/doctores/admin"), {
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

  return response.json() as Promise<DoctorRegistrationResult>;
}

