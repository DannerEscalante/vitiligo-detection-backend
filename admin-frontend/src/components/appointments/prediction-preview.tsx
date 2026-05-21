"use client";

import { useState } from "react";
import { Microscope } from "lucide-react";

import { buildMediaUrl } from "@/lib/media-url";
import { formatPredictionResult } from "@/lib/prediction-format";
import type { PredictionSummary } from "@/types/appointments";

interface PredictionPreviewProps {
  prediction: PredictionSummary | null;
  appointmentDate?: string;
  onImageClick?: (payload: {
    prediction: PredictionSummary;
    imageUrl: string;
    appointmentDate?: string;
  }) => void;
}

export function PredictionPreview({
  prediction,
  appointmentDate,
  onImageClick
}: PredictionPreviewProps) {
  const [imageFailed, setImageFailed] = useState(false);

  if (!prediction) {
    return <span className="text-sm text-muted-foreground">Sin analisis</span>;
  }

  const imageUrl = buildMediaUrl(prediction.imagen);
  const hasImageUrl = Boolean(imageUrl);
  const canShowImage = hasImageUrl && !imageFailed;
  const confidence = Math.round(prediction.confianza * 100);
  const resultLabel = formatPredictionResult(prediction.resultado);

  const fallback = (
    <div className="flex h-full w-full flex-col items-center justify-center bg-teal-50 text-teal-700">
      <Microscope className="h-5 w-5" aria-hidden="true" />
      <span className="mt-0.5 text-[10px] font-medium">IA</span>
    </div>
  );

  const thumbnail = canShowImage ? (
    <button
      type="button"
      className="h-full w-full cursor-zoom-in overflow-hidden"
      onClick={() => {
        if (imageUrl) {
          onImageClick?.({ prediction, imageUrl, appointmentDate });
        }
      }}
      aria-label="Ver imagen dermatologica"
    >
      {/* La URL puede venir desde FastAPI como ruta relativa bajo /uploads. */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={imageUrl ?? ""}
        alt=""
        className="h-full w-full object-cover"
        onError={() => setImageFailed(true)}
      />
    </button>
  ) : hasImageUrl ? (
    <button
      type="button"
      className="h-full w-full cursor-zoom-in overflow-hidden"
      onClick={() => {
        if (imageUrl) {
          onImageClick?.({ prediction, imageUrl, appointmentDate });
        }
      }}
      aria-label="Ver imagen dermatologica"
    >
      {fallback}
    </button>
  ) : (
    fallback
  );

  return (
    <div className="flex min-w-48 items-center gap-3">
      <div className="flex h-14 w-14 shrink-0 items-center justify-center overflow-hidden rounded-md border bg-muted shadow-sm">
        {thumbnail}
      </div>
      <div className="min-w-0">
        <p className="truncate text-sm font-medium">{resultLabel}</p>
        <p className="text-xs text-muted-foreground">{confidence}% confianza</p>
      </div>
    </div>
  );
}
