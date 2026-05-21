import type { ComponentProps } from "react";
import { Activity, FileText } from "lucide-react";

import { TreatmentStatusBadge } from "@/components/patients/treatment-status-badge";
import { TreatmentPredictionsGallery } from "@/components/patients/treatment-predictions-gallery";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { formatClinicalDate } from "@/lib/patient-format";
import type { ActiveTreatment, ClinicalHistory } from "@/types/patients";

interface PatientTreatmentCardProps {
  treatment: ActiveTreatment | null;
  history: ClinicalHistory[];
  onImageClick: ComponentProps<typeof TreatmentPredictionsGallery>["onImageClick"];
}

export function PatientTreatmentCard({
  treatment,
  history,
  onImageClick
}: PatientTreatmentCardProps) {
  const active = treatment?.tiene_tratamiento ?? false;
  const activeTreatmentRecord = history
    .flatMap((item) =>
      item.tratamientos.map((clinicalTreatment) => ({
        ...clinicalTreatment,
        historyDate: item.fecha
      }))
    )
    .find((clinicalTreatment) => clinicalTreatment.id === treatment?.tratamiento_id);

  return (
    <Card>
      <CardHeader className="flex flex-row items-start justify-between space-y-0">
        <div>
          <CardTitle>Tratamiento actual</CardTitle>
          <CardDescription>Estado clinico registrado para el paciente.</CardDescription>
        </div>
        <TreatmentStatusBadge active={active} />
      </CardHeader>
      <CardContent className="space-y-4">
        {active ? (
          <>
            <div className="grid gap-3 sm:grid-cols-3">
              <div className="rounded-md border p-3">
                <p className="text-xs font-medium uppercase text-muted-foreground">Tipo</p>
                <p className="mt-1 text-sm font-semibold">
                  {treatment?.tipo_tratamiento ?? "No especificado"}
                </p>
              </div>
              <div className="rounded-md border p-3">
                <p className="text-xs font-medium uppercase text-muted-foreground">Inicio</p>
                <p className="mt-1 text-sm font-semibold">
                  {formatClinicalDate(treatment?.fecha_inicio ?? null)}
                </p>
              </div>
              <div className="rounded-md border p-3">
                <p className="text-xs font-medium uppercase text-muted-foreground">Estado</p>
                <p className="mt-1 text-sm font-semibold">{treatment?.estado ?? "Activo"}</p>
              </div>
            </div>
            <div className="rounded-md border border-teal-100 bg-teal-50 p-4">
              <div className="flex items-center gap-2 text-teal-800">
                <FileText className="h-4 w-4" aria-hidden="true" />
                <p className="text-sm font-semibold">Observaciones clinicas</p>
              </div>
              <p className="mt-2 text-sm text-teal-950">
                {treatment?.notas ?? "Sin observaciones registradas."}
              </p>
            </div>
            <div className="space-y-3">
              <div>
                <p className="text-sm font-semibold">Imagenes del tratamiento actual</p>
                <p className="text-sm text-muted-foreground">
                  Predicciones e imagenes registradas dentro del tratamiento activo.
                </p>
              </div>
              <TreatmentPredictionsGallery
                predictions={activeTreatmentRecord?.predicciones ?? []}
                fallbackDate={activeTreatmentRecord?.historyDate}
                compact
                onImageClick={onImageClick}
              />
            </div>
          </>
        ) : (
          <div className="flex items-center gap-3 rounded-md border border-dashed p-4 text-muted-foreground">
            <Activity className="h-5 w-5" aria-hidden="true" />
            <p className="text-sm">No existe tratamiento activo registrado.</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
