"use client";

import type { ComponentProps } from "react";
import { useState } from "react";
import { AlertCircle, RefreshCw } from "lucide-react";

import { ImagePreviewDialog } from "@/components/appointments/image-preview-dialog";
import { PatientClinicalRecord } from "@/components/patients/patient-clinical-record";
import { PatientsTable } from "@/components/patients/patients-table";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { usePatients } from "@/hooks/use-patients";

export function PatientsDashboard() {
  const [selectedImagePreview, setSelectedImagePreview] = useState<ComponentProps<
    typeof ImagePreviewDialog
  >["preview"]>(null);

  const {
    patients,
    selectedPatient,
    selectedHistory,
    selectedTreatment,
    isLoadingPatients,
    isLoadingRecord,
    error,
    reload,
    selectPatient
  } = usePatients();

  return (
    <>
      <div className="grid gap-6 xl:grid-cols-[360px_1fr]">
        <Card className="h-fit">
          <CardHeader className="gap-4">
            <div>
              <CardTitle>Pacientes</CardTitle>
              <CardDescription>Registro administrativo de pacientes.</CardDescription>
            </div>
            <Button variant="outline" onClick={() => void reload()} disabled={isLoadingPatients}>
              <RefreshCw className={isLoadingPatients ? "animate-spin" : ""} />
              Actualizar
            </Button>
          </CardHeader>
          <CardContent>
            {error ? (
              <div className="mb-4 flex items-start gap-3 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
                <p>{error}</p>
              </div>
            ) : null}

            {isLoadingPatients ? (
              <div className="grid gap-3">
                {Array.from({ length: 6 }).map((_, index) => (
                  <div key={index} className="h-16 animate-pulse rounded-md bg-muted" />
                ))}
              </div>
            ) : (
              <PatientsTable
                patients={patients}
                selectedPatientId={selectedPatient?.id ?? null}
                onSelectPatient={selectPatient}
              />
            )}
          </CardContent>
        </Card>

        <PatientClinicalRecord
          patient={selectedPatient}
          history={selectedHistory}
          treatment={selectedTreatment}
          isLoading={isLoadingRecord}
          onImageClick={setSelectedImagePreview}
        />
      </div>

      <ImagePreviewDialog
        preview={selectedImagePreview}
        onClose={() => setSelectedImagePreview(null)}
      />
    </>
  );
}
