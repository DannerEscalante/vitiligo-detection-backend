"use client";

import { ImageIcon } from "lucide-react";

import { buildMediaUrl } from "@/lib/media-url";
import { formatClinicalDate } from "@/lib/patient-format";
import type { ClinicalHistory, ClinicalPrediction } from "@/types/patients";

interface PatientPhotoEvolutionProps {
  history: ClinicalHistory[];
  onImageClick: (payload: {
    prediction: {
      resultado: string;
      confianza: number;
      imagen: string | null;
    };
    imageUrl: string;
    appointmentDate?: string;
  }) => void;
}

export function PatientPhotoEvolution({ history, onImageClick }: PatientPhotoEvolutionProps) {
  const predictions = history
    .flatMap((item) =>
      item.tratamientos.flatMap((treatment) =>
        treatment.predicciones.map((prediction) => ({
          ...prediction,
          treatmentName: treatment.tipo_tratamiento,
          historyDate: item.fecha
        }))
      )
    )
    .sort((a, b) => {
      const dateA = new Date(a.fecha ?? a.historyDate).getTime();
      const dateB = new Date(b.fecha ?? b.historyDate).getTime();
      return dateA - dateB;
    });

  if (predictions.length === 0) {
    return (
      <div className="flex min-h-40 flex-col items-center justify-center rounded-md border border-dashed bg-white p-6 text-center">
        <ImageIcon className="h-9 w-9 text-muted-foreground" aria-hidden="true" />
        <p className="mt-3 text-sm font-medium">Sin predicciones registradas</p>
        <p className="mt-1 text-sm text-muted-foreground">
          La evolucion fotografica se mostrara cronologicamente cuando existan imagenes.
        </p>
      </div>
    );
  }

  return (
    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
      {predictions.map((prediction, index) => (
        <PhotoCard
          key={`${prediction.resultado}-${prediction.fecha ?? prediction.historyDate}-${index}`}
          prediction={prediction}
          onImageClick={onImageClick}
        />
      ))}
    </div>
  );
}

function PhotoCard({
  prediction,
  onImageClick
}: {
  prediction: ClinicalPrediction & { treatmentName?: string | null; historyDate: string };
  onImageClick: PatientPhotoEvolutionProps["onImageClick"];
}) {
  const imageUrl = buildMediaUrl(prediction.imagen);
  const confidence = Math.round(prediction.confianza * 100);
  const date = prediction.fecha ?? prediction.historyDate;

  return (
    <article className="overflow-hidden rounded-md border bg-white">
      <button
        type="button"
        disabled={!imageUrl}
        onClick={() => {
          if (imageUrl) {
            onImageClick({
              prediction,
              imageUrl,
              appointmentDate: date
            });
          }
        }}
        className="flex aspect-[4/3] w-full items-center justify-center bg-muted disabled:cursor-default"
      >
        {imageUrl ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={imageUrl} alt="" className="h-full w-full object-cover" />
        ) : (
          <ImageIcon className="h-8 w-8 text-muted-foreground" aria-hidden="true" />
        )}
      </button>
      <div className="space-y-1 p-3">
        <p className="truncate text-sm font-semibold">{prediction.resultado}</p>
        <p className="text-xs text-muted-foreground">{confidence}% confianza</p>
        <p className="text-xs text-muted-foreground">{formatClinicalDate(date)}</p>
      </div>
    </article>
  );
}
