import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const statusMeta = [
  { key: "pendiente", label: "Pendientes", className: "bg-amber-500" },
  { key: "confirmada", label: "Confirmadas", className: "bg-teal-600" },
  { key: "finalizada", label: "Finalizadas", className: "bg-slate-500" },
  { key: "cancelada", label: "Canceladas", className: "bg-red-500" }
] as const;

interface AppointmentsStatusCardProps {
  counts: Record<(typeof statusMeta)[number]["key"], number>;
}

export function AppointmentsStatusCard({ counts }: AppointmentsStatusCardProps) {
  const total = Object.values(counts).reduce((sum, value) => sum + value, 0);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Estado de citas</CardTitle>
        <CardDescription>Distribucion operativa de citas registradas.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {statusMeta.map((status) => {
          const percentage = total > 0 ? Math.round((counts[status.key] / total) * 100) : 0;

          return (
            <div key={status.key} className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="font-medium">{status.label}</span>
                <span className="text-muted-foreground">
                  {counts[status.key]} · {percentage}%
                </span>
              </div>
              <div className="h-2 rounded-full bg-muted">
                <div
                  className={`h-2 rounded-full ${status.className}`}
                  style={{ width: `${Math.max(percentage, counts[status.key] > 0 ? 6 : 0)}%` }}
                />
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}
