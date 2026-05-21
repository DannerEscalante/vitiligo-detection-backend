import { Badge } from "@/components/ui/badge";

export function TreatmentStatusBadge({ active }: { active: boolean }) {
  return (
    <Badge
      variant="outline"
      className={
        active
          ? "border-teal-200 bg-teal-50 text-teal-700"
          : "border-slate-200 bg-slate-100 text-slate-600"
      }
    >
      {active ? "Activo" : "Sin activo"}
    </Badge>
  );
}
