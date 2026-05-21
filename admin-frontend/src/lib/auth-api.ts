import { getApiUrl } from "@/lib/api";

interface LoginResponse {
  access_token: string;
  refresh_token: string;
  rol_id: number;
  token_type: string;
}

async function parseApiError(response: Response) {
  try {
    const body = await response.json();
    return body.detail ?? `Error HTTP ${response.status}`;
  } catch {
    return `Error HTTP ${response.status}`;
  }
}

export async function loginAdmin(email: string, password: string) {
  const response = await fetch(getApiUrl("/login"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      email,
      contrasena: password
    })
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<LoginResponse>;
}
