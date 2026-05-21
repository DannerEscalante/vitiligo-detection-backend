"use client";

import { UserRound } from "lucide-react";

import { TreatmentStatusBadge } from "@/components/patients/treatment-status-badge";
import { calculateAge } from "@/lib/patient-format";
import { cn } from "@/lib/utils";
import type { PatientWithTreatment } from "@/types/patients";

interface PatientsTableProps {
  patients: PatientWithTreatment[];
  selectedPatientId: number | null;
  onSelectPatient: (patientId: number) => void;
}

export function PatientsTable({
  patients,
  selectedPatientId,
  onSelectPatient
}: PatientsTableProps) {
  if (patients.length === 0) {
    return (
      <div className="flex min-h-64 flex-col items-center justify-center rounded-md border border-dashed bg-white p-6 text-center">
        <UserRound className="h-10 w-10 text-muted-foreground" aria-hidden="true" />
        <h3 className="mt-4 text-base font-semibold">No hay pacientes registrados</h3>
        <p className="mt-1 text-sm text-muted-foreground">
          Los pacientes apareceran cuando existan registros en el backend.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-md border bg-white">
      <div className="max-h-[68vh] overflow-y-auto">
        {patients.map((patient) => {
          const isSelected = patient.id === selectedPatientId;
          const activeTreatment = patient.tratamiento_activo?.tiene_tratamiento ?? false;

          return (
            <button
              key={patient.id}
              type="button"
              onClick={() => onSelectPatient(patient.id)}
              className={cn(
                "block w-full border-b px-4 py-4 text-left transition-colors last:border-b-0",
                isSelected ? "bg-teal-50" : "bg-white hover:bg-muted/70"
              )}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="truncate text-sm font-semibold">{patient.nombre}</p>
                  <p className="mt-1 text-xs text-muted-foreground">
                    {patient.sexo ?? "Sexo no registrado"} · {calculateAge(patient.fecha_nacimiento)}
                  </p>
                </div>
                <TreatmentStatusBadge active={activeTreatment} />
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
