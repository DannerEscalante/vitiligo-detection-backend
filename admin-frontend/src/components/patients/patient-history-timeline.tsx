import type { ComponentProps } from "react";
import { FileText } from "lucide-react";

import { TreatmentPredictionsGallery } from "@/components/patients/treatment-predictions-gallery";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { formatClinicalDate } from "@/lib/patient-format";
import type { ClinicalHistory } from "@/types/patients";

const treatmentStatusClasses: Record<string, string> = {
  activo: "border-teal-200 bg-teal-50 text-teal-700",
  finalizado: "border-slate-200 bg-slate-100 text-slate-600"
};

interface PatientHistoryTimelineProps {
  history: ClinicalHistory[];
  excludeTreatmentId?: number | null;
  onImageClick: ComponentProps<typeof TreatmentPredictionsGallery>["onImageClick"];
}

export function PatientHistoryTimeline({
  history,
  excludeTreatmentId,
  onImageClick
}: PatientHistoryTimelineProps) {
  const visibleHistory = history
    .map((item) => ({
      ...item,
      tratamientos: item.tratamientos.filter(
        (treatment) => treatment.id !== excludeTreatmentId
      )
    }))
    .filter((item) => item.tratamientos.length > 0);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Historial clinico</CardTitle>
        <CardDescription>
          Diagnosticos, tratamientos, observaciones e imagenes asociadas a cada tratamiento.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {visibleHistory.length === 0 ? (
          <div className="flex items-center gap-3 rounded-md border border-dashed p-4 text-muted-foreground">
            <FileText className="h-5 w-5" aria-hidden="true" />
            <p className="text-sm">No hay tratamientos historicos adicionales registrados.</p>
          </div>
        ) : (
          <div className="space-y-5">
            {visibleHistory.map((item) => (
              <article key={item.id} className="relative border-l pl-5">
                <span className="absolute -left-1.5 top-1 h-3 w-3 rounded-full bg-primary" />
                <div className="rounded-md border bg-white p-4">
                  <div className="flex flex-wrap items-start justify-between gap-2">
                    <div>
                      <p className="text-sm font-semibold">{item.diagnostico}</p>
                      <p className="mt-1 text-xs text-muted-foreground">
                        {formatClinicalDate(item.fecha)}
                      </p>
                    </div>
                    <Badge variant="outline">{item.tratamientos.length} tratamientos</Badge>
                  </div>

                  <div className="mt-4 space-y-3">
                    {item.tratamientos.map((treatment) => (
                      <div key={treatment.id} className="rounded-md border bg-muted/30 p-3">
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <p className="text-sm font-medium">
                            {treatment.tipo_tratamiento ?? "Tratamiento sin tipo"}
                          </p>
                          <Badge
                            variant="outline"
                            className={
                              treatmentStatusClasses[treatment.estado] ??
                              "border-slate-200 bg-slate-100 text-slate-600"
                            }
                          >
                            {treatment.estado}
                          </Badge>
                        </div>
                        <div className="mt-3 grid gap-2 text-xs text-muted-foreground sm:grid-cols-2">
                          <p>Inicio: {formatClinicalDate(treatment.fecha_inicio)}</p>
                          <p>Fin: {formatClinicalDate(treatment.fecha_fin)}</p>
                        </div>
                        <div className="mt-3 rounded-md border bg-white p-3">
                          <p className="text-xs font-medium uppercase text-muted-foreground">
                            Observaciones clinicas
                          </p>
                          <p className="mt-1 text-sm">
                            {treatment.notas ?? "Sin observaciones registradas."}
                          </p>
                        </div>
                        <div className="mt-3 space-y-2">
                          <p className="text-xs font-medium uppercase text-muted-foreground">
                            Imagenes y predicciones del tratamiento
                          </p>
                          <TreatmentPredictionsGallery
                            predictions={treatment.predicciones}
                            fallbackDate={item.fecha}
                            onImageClick={onImageClick}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
