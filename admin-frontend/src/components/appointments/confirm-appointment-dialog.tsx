"use client";

import { useEffect, useState } from "react";
import { CalendarCheck, X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { PredictionPreview } from "@/components/appointments/prediction-preview";
import { StatusBadge } from "@/components/appointments/status-badge";
import { formatAppointmentDateTime } from "@/lib/date-format";
import type { Appointment, DoctorSummary } from "@/types/appointments";

interface ConfirmAppointmentDialogProps {
  appointment: Appointment | null;
  doctors: DoctorSummary[];
  isConfirming: boolean;
  onClose: () => void;
  onConfirm: (doctorId: number) => void;
}

export function ConfirmAppointmentDialog({
  appointment,
  doctors,
  isConfirming,
  onClose,
  onConfirm
}: ConfirmAppointmentDialogProps) {
  const [selectedDoctorId, setSelectedDoctorId] = useState("");

  useEffect(() => {
    setSelectedDoctorId("");
  }, [appointment?.id]);

  if (!appointment) {
    return null;
  }

  const canConfirm = Boolean(selectedDoctorId) && !isConfirming;
  const selectedDoctor = doctors.find((doctor) => String(doctor.id) === selectedDoctorId);
  const dateParts = formatAppointmentDateTime(appointment.fecha_hora);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/45 p-4">
      <div className="w-full max-w-2xl rounded-lg border bg-white shadow-xl">
        <div className="flex items-start justify-between border-b p-5">
          <div>
            <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-md bg-primary text-primary-foreground">
              <CalendarCheck className="h-5 w-5" aria-hidden="true" />
            </div>
            <h2 className="text-lg font-semibold">Confirmar cita</h2>
            <p className="text-sm text-muted-foreground">
              Selecciona el doctor responsable para esta consulta.
            </p>
          </div>
          <Button variant="ghost" size="icon" onClick={onClose} aria-label="Cerrar">
            <X />
          </Button>
        </div>

        <div className="space-y-5 p-5">
          <div className="grid gap-3 rounded-md border bg-muted/30 p-4 sm:grid-cols-2">
            <div>
              <p className="text-xs font-medium uppercase text-muted-foreground">Paciente</p>
              <p className="mt-1 text-sm font-semibold">
                {appointment.paciente?.nombre ?? "Paciente no disponible"}
              </p>
            </div>
            <div>
              <p className="text-xs font-medium uppercase text-muted-foreground">Fecha y hora</p>
              <p className="mt-1 text-sm font-semibold">{dateParts.label}</p>
            </div>
            <div>
              <p className="text-xs font-medium uppercase text-muted-foreground">Estado</p>
              <div className="mt-2">
                <StatusBadge status={appointment.estado} />
              </div>
            </div>
            <div>
              <p className="text-xs font-medium uppercase text-muted-foreground">Analisis IA</p>
              <div className="mt-2">
                <PredictionPreview prediction={appointment.prediccion} />
              </div>
            </div>
          </div>

          <label className="block space-y-2">
            <span className="text-sm font-medium">Doctor asignado</span>
            <select
              value={selectedDoctorId}
              onChange={(event) => setSelectedDoctorId(event.target.value)}
              className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm outline-none ring-offset-background focus:ring-2 focus:ring-ring"
            >
              <option value="">Seleccionar doctor</option>
              {doctors.map((doctor) => (
                <option key={doctor.id} value={doctor.id}>
                  {doctor.nombre}
                </option>
              ))}
            </select>
          </label>

          <div className="rounded-md border border-teal-100 bg-teal-50 px-4 py-3">
            <p className="text-xs font-medium uppercase text-teal-700">Doctor seleccionado</p>
            <p className="mt-1 text-sm font-semibold text-teal-950">
              {selectedDoctor?.nombre ?? "Selecciona un doctor para continuar"}
            </p>
          </div>

          {doctors.length === 0 ? (
            <p className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-700">
              No hay doctores disponibles para asignar.
            </p>
          ) : null}
        </div>

        <div className="flex justify-end gap-2 border-t p-5">
          <Button variant="outline" onClick={onClose} disabled={isConfirming}>
            Cancelar
          </Button>
          <Button
            onClick={() => onConfirm(Number(selectedDoctorId))}
            disabled={!canConfirm}
          >
            {isConfirming ? "Confirmando..." : "Confirmar cita"}
          </Button>
        </div>
      </div>
    </div>
  );
}
