"use client";

import { ImageIcon } from "lucide-react";

import { buildMediaUrl } from "@/lib/media-url";
import { formatClinicalDate } from "@/lib/patient-format";
import { formatPredictionResult } from "@/lib/prediction-format";
import type { ClinicalPrediction } from "@/types/patients";

interface TreatmentPredictionsGalleryProps {
  predictions: ClinicalPrediction[];
  fallbackDate?: string;
  compact?: boolean;
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

export function TreatmentPredictionsGallery({
  predictions,
  fallbackDate,
  compact = false,
  onImageClick
}: TreatmentPredictionsGalleryProps) {
  if (predictions.length === 0) {
    return (
      <div className="flex items-center gap-3 rounded-md border border-dashed bg-white p-4 text-muted-foreground">
        <ImageIcon className="h-5 w-5 shrink-0" aria-hidden="true" />
        <p className="text-sm">Sin imagenes registradas para este tratamiento.</p>
      </div>
    );
  }

  return (
    <div
      className={
        compact
          ? "grid gap-3 sm:grid-cols-3 xl:grid-cols-4"
          : "grid gap-3 sm:grid-cols-2 xl:grid-cols-3"
      }
    >
      {predictions.map((prediction, index) => {
        const imageUrl = buildMediaUrl(prediction.imagen);
        const date = prediction.fecha ?? fallbackDate;
        const confidence = Math.round(prediction.confianza * 100);
        const resultLabel = formatPredictionResult(prediction.resultado);

        return (
          <article
            key={`${prediction.resultado}-${date ?? "sin-fecha"}-${index}`}
            className="overflow-hidden rounded-md border bg-white"
          >
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
              <p className="truncate text-sm font-semibold">{resultLabel}</p>
              <p className="text-xs text-muted-foreground">{confidence}% confianza</p>
              <p className="text-xs text-muted-foreground">{formatClinicalDate(date ?? null)}</p>
            </div>
          </article>
        );
      })}
    </div>
  );
}
