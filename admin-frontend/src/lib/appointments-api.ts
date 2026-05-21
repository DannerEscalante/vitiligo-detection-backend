import { getApiUrl } from "@/lib/api";
import { getStoredAccessToken } from "@/lib/auth-token";
import type { Appointment } from "@/types/appointments";

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

export async function getAppointments() {
  const response = await fetch(getApiUrl("/citas/"), {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<Appointment[]>;
}

export async function confirmAppointment(appointmentId: number, doctorId: number) {
  const response = await fetch(
    getApiUrl(`/citas/${appointmentId}/confirmar/?doctor_id=${doctorId}`),
    {
      method: "PATCH",
      headers: getAuthHeaders()
    }
  );

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<Appointment>;
}
