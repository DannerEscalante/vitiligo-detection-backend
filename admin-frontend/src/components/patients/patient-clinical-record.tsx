"use client";

import type { ComponentProps } from "react";
import { Loader2, UserRound } from "lucide-react";

import { PatientHistoryTimeline } from "@/components/patients/patient-history-timeline";
import { PatientTreatmentCard } from "@/components/patients/patient-treatment-card";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { calculateAge, formatClinicalDate } from "@/lib/patient-format";
import type { ActiveTreatment, ClinicalHistory, PatientWithTreatment } from "@/types/patients";

interface PatientClinicalRecordProps {
  patient: PatientWithTreatment | null;
  history: ClinicalHistory[];
  treatment: ActiveTreatment | null;
  isLoading: boolean;
  onImageClick: ComponentProps<typeof PatientHistoryTimeline>["onImageClick"];
}

export function PatientClinicalRecord({
  patient,
  history,
  treatment,
  isLoading,
  onImageClick
}: PatientClinicalRecordProps) {
  if (!patient) {
    return (
      <Card className="min-h-[540px]">
        <CardContent className="flex min-h-[540px] flex-col items-center justify-center text-center">
          <UserRound className="h-10 w-10 text-muted-foreground" aria-hidden="true" />
          <h3 className="mt-4 text-base font-semibold">Selecciona un paciente</h3>
          <p className="mt-1 max-w-sm text-sm text-muted-foreground">
            El expediente clinico se abrira aqui sin cambiar de pagina.
          </p>
        </CardContent>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card className="min-h-[540px]">
        <CardContent className="flex min-h-[540px] items-center justify-center gap-2 text-muted-foreground">
          <Loader2 className="h-5 w-5 animate-spin" aria-hidden="true" />
          <span className="text-sm">Cargando expediente clinico...</span>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-5">
      <Card>
        <CardHeader className="gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <CardTitle>{patient.nombre}</CardTitle>
            <CardDescription>Expediente medico administrativo</CardDescription>
          </div>
          <div className="rounded-md border bg-muted/40 px-3 py-2 text-sm">
            ID paciente: <span className="font-semibold">{patient.id}</span>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid gap-3 sm:grid-cols-3">
            <div className="rounded-md border p-3">
              <p className="text-xs font-medium uppercase text-muted-foreground">Sexo</p>
              <p className="mt-1 text-sm font-semibold">{patient.sexo ?? "No registrado"}</p>
            </div>
            <div className="rounded-md border p-3">
              <p className="text-xs font-medium uppercase text-muted-foreground">Edad</p>
              <p className="mt-1 text-sm font-semibold">
                {calculateAge(patient.fecha_nacimiento)}
              </p>
            </div>
            <div className="rounded-md border p-3">
              <p className="text-xs font-medium uppercase text-muted-foreground">Nacimiento</p>
              <p className="mt-1 text-sm font-semibold">
                {formatClinicalDate(patient.fecha_nacimiento)}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      <PatientTreatmentCard
        treatment={treatment}
        history={history}
        onImageClick={onImageClick}
      />

      <PatientHistoryTimeline
        history={history}
        excludeTreatmentId={treatment?.tratamiento_id}
        onImageClick={onImageClick}
      />
    </div>
  );
}
