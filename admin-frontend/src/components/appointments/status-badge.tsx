import { Badge } from "@/components/ui/badge";
import type { AppointmentStatus } from "@/types/appointments";

const statusLabels: Record<AppointmentStatus, string> = {
  pendiente: "Pendiente",
  confirmada: "Confirmada",
  finalizada: "Finalizada",
  cancelada: "Cancelada"
};

const statusClasses: Record<AppointmentStatus, string> = {
  pendiente: "border-amber-200 bg-amber-50 text-amber-700",
  confirmada: "border-teal-200 bg-teal-50 text-teal-700",
  finalizada: "border-slate-200 bg-slate-100 text-slate-600",
  cancelada: "border-red-200 bg-red-50 text-red-700"
};

export function StatusBadge({ status }: { status: AppointmentStatus }) {
  return (
    <Badge variant="outline" className={statusClasses[status]}>
      {statusLabels[status] ?? status}
    </Badge>
  );
}
