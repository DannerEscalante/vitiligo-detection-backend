"use client";

import { CalendarClock } from "lucide-react";

import { Button } from "@/components/ui/button";
import { PredictionPreview } from "@/components/appointments/prediction-preview";
import { StatusBadge } from "@/components/appointments/status-badge";
import { formatAppointmentDateTime } from "@/lib/date-format";
import type { Appointment, PredictionSummary } from "@/types/appointments";

interface AppointmentsTableProps {
  appointments: Appointment[];
  onConfirm: (appointment: Appointment) => void;
  onImageClick: (payload: {
    prediction: PredictionSummary;
    imageUrl: string;
    appointmentDate?: string;
  }) => void;
}

export function AppointmentsTable({
  appointments,
  onConfirm,
  onImageClick
}: AppointmentsTableProps) {
  if (appointments.length === 0) {
    return (
      <div className="flex min-h-64 flex-col items-center justify-center rounded-md border border-dashed bg-white p-8 text-center">
        <CalendarClock className="h-10 w-10 text-muted-foreground" aria-hidden="true" />
        <h3 className="mt-4 text-base font-semibold">No hay citas para este filtro</h3>
        <p className="mt-1 max-w-sm text-sm text-muted-foreground">
          Cuando existan citas reales en el backend apareceran en esta tabla.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-md border bg-white">
      <div className="overflow-x-auto">
        <table className="w-full min-w-[920px] text-sm">
          <thead className="bg-muted text-left text-muted-foreground">
            <tr>
              <th className="px-4 py-3 font-medium">Paciente</th>
              <th className="px-4 py-3 font-medium">Fecha</th>
              <th className="px-4 py-3 font-medium">Hora</th>
              <th className="px-4 py-3 font-medium">Estado</th>
              <th className="px-4 py-3 font-medium">Doctor</th>
              <th className="px-4 py-3 font-medium">Analisis IA</th>
              <th className="px-4 py-3 text-right font-medium">Acciones</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {appointments.map((appointment) => {
              const dateParts = formatAppointmentDateTime(appointment.fecha_hora);

              return (
                <tr key={appointment.id} className="align-middle">
                  <td className="px-4 py-4">
                    <p className="font-medium">
                      {appointment.paciente?.nombre ?? "Paciente no disponible"}
                    </p>
                    {appointment.paciente?.sexo ? (
                      <p className="text-xs text-muted-foreground">{appointment.paciente.sexo}</p>
                    ) : null}
                  </td>
                  <td className="px-4 py-4 text-muted-foreground">{dateParts.date}</td>
                  <td className="px-4 py-4 font-medium">{dateParts.time}</td>
                  <td className="px-4 py-4">
                    <StatusBadge status={appointment.estado} />
                  </td>
                  <td className="px-4 py-4">
                    {appointment.doctor?.nombre ?? (
                      <span className="text-muted-foreground">Sin asignar</span>
                    )}
                  </td>
                  <td className="px-4 py-4">
                    <PredictionPreview
                      prediction={appointment.prediccion}
                      appointmentDate={appointment.fecha_hora}
                      onImageClick={onImageClick}
                    />
                  </td>
                  <td className="px-4 py-4 text-right">
                    {appointment.estado === "pendiente" ? (
                      <Button size="sm" onClick={() => onConfirm(appointment)}>
                        Confirmar
                      </Button>
                    ) : (
                      <span className="text-xs text-muted-foreground">Sin acciones</span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
