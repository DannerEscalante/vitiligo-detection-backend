import { StatusBadge } from "@/components/appointments/status-badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { formatAppointmentDateTime } from "@/lib/date-format";
import type { Appointment } from "@/types/appointments";

export function RecentActivityCard({ appointments }: { appointments: Appointment[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Actividad reciente</CardTitle>
        <CardDescription>Ultimas citas registradas en el sistema.</CardDescription>
      </CardHeader>
      <CardContent>
        {appointments.length === 0 ? (
          <div className="rounded-md border border-dashed p-5 text-sm text-muted-foreground">
            No hay citas registradas.
          </div>
        ) : (
          <div className="overflow-hidden rounded-md border">
            <table className="w-full min-w-[620px] text-sm">
              <thead className="bg-muted text-left text-muted-foreground">
                <tr>
                  <th className="px-4 py-3 font-medium">Paciente</th>
                  <th className="px-4 py-3 font-medium">Fecha</th>
                  <th className="px-4 py-3 font-medium">Doctor</th>
                  <th className="px-4 py-3 font-medium">Estado</th>
                </tr>
              </thead>
              <tbody className="divide-y bg-white">
                {appointments.map((appointment) => {
                  const date = formatAppointmentDateTime(appointment.fecha_hora);

                  return (
                    <tr key={appointment.id}>
                      <td className="px-4 py-3 font-medium">
                        {appointment.paciente?.nombre ?? "Paciente no disponible"}
                      </td>
                      <td className="px-4 py-3 text-muted-foreground">{date.label}</td>
                      <td className="px-4 py-3">
                        {appointment.doctor?.nombre ?? (
                          <span className="text-muted-foreground">Sin asignar</span>
                        )}
                      </td>
                      <td className="px-4 py-3">
                        <StatusBadge status={appointment.estado} />
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
