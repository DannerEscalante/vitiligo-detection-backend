const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export function buildMediaUrl(path: string | null) {
  if (!path) {
    return null;
  }

  const normalizedSlashes = path.replaceAll("\\", "/");

  if (normalizedSlashes.startsWith("http://") || normalizedSlashes.startsWith("https://")) {
    return normalizedSlashes;
  }

  const normalizedPath = normalizedSlashes.startsWith("/")
    ? normalizedSlashes
    : `/${normalizedSlashes}`;

  return `${API_BASE_URL}${normalizedPath}`;
}
