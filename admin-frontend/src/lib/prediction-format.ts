export function formatPredictionResult(result: string) {
  const normalized = result.trim().toLowerCase();

  if (normalized === "vitiligo") {
    return "Vitiligo";
  }

  if (normalized === "no_vitiligo" || normalized === "no vitiligo") {
    return "No vitiligo";
  }

  return result
    .replaceAll("_", " ")
    .split(" ")
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(" ");
}
