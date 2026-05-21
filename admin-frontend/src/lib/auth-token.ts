const TOKEN_KEYS = ["access_token", "accessToken", "token"];

export function getStoredAccessToken() {
  if (typeof window === "undefined") {
    return null;
  }

  for (const key of TOKEN_KEYS) {
    const token = window.localStorage.getItem(key);
    if (token) {
      return token;
    }
  }

  return null;
}
