"use client";

import { useState } from "react";
import { AlertCircle, RefreshCw } from "lucide-react";

import { AppointmentStatusFilter } from "@/components/appointments/appointment-status-filter";
import { AppointmentsTable } from "@/components/appointments/appointments-table";
import { ConfirmAppointmentDialog } from "@/components/appointments/confirm-appointment-dialog";
import { ImagePreviewDialog } from "@/components/appointments/image-preview-dialog";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAppointments } from "@/hooks/use-appointments";
import type { PredictionSummary } from "@/types/appointments";

export function AppointmentsDashboard() {
  const [selectedImagePreview, setSelectedImagePreview] = useState<{
    prediction: PredictionSummary;
    imageUrl: string;
    appointmentDate?: string;
  } | null>(null);

  const {
    doctors,
    filteredAppointments,
    selectedStatus,
    selectedAppointment,
    isLoading,
    isConfirming,
    error,
    successMessage,
    statusCounts,
    setSelectedStatus,
    setSelectedAppointment,
    setSuccessMessage,
    reload,
    confirmSelectedAppointment
  } = useAppointments();

  return (
    <>
      <Card>
        <CardHeader className="gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <CardTitle>Citas medicas</CardTitle>
            <CardDescription>
              Confirmacion administrativa, asignacion de doctores y revision de analisis IA.
            </CardDescription>
          </div>
          <Button variant="outline" onClick={() => void reload()} disabled={isLoading}>
            <RefreshCw className={isLoading ? "animate-spin" : ""} />
            Actualizar
          </Button>
        </CardHeader>
        <CardContent className="space-y-5">
          <AppointmentStatusFilter
            selectedStatus={selectedStatus}
            counts={statusCounts}
            onChange={setSelectedStatus}
          />

          {successMessage ? (
            <div className="flex items-center justify-between rounded-md border border-teal-200 bg-teal-50 px-4 py-3 text-sm text-teal-700">
              <span>{successMessage}</span>
              <button type="button" onClick={() => setSuccessMessage(null)} className="font-medium">
                Cerrar
              </button>
            </div>
          ) : null}

          {error ? (
            <div className="flex items-start gap-3 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
              <div>
                <p className="font-medium">No se pudo completar la operacion</p>
                <p>{error}</p>
              </div>
            </div>
          ) : null}

          {isLoading ? (
            <div className="grid gap-3">
              {Array.from({ length: 5 }).map((_, index) => (
                <div key={index} className="h-16 animate-pulse rounded-md bg-muted" />
              ))}
            </div>
          ) : (
            <AppointmentsTable
              appointments={filteredAppointments}
              onConfirm={setSelectedAppointment}
              onImageClick={setSelectedImagePreview}
            />
          )}
        </CardContent>
      </Card>

      <ConfirmAppointmentDialog
        appointment={selectedAppointment}
        doctors={doctors}
        isConfirming={isConfirming}
        onClose={() => setSelectedAppointment(null)}
        onConfirm={(doctorId) => void confirmSelectedAppointment(doctorId)}
      />

      <ImagePreviewDialog
        preview={selectedImagePreview}
        onClose={() => setSelectedImagePreview(null)}
      />
    </>
  );
}
