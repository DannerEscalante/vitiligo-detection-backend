"use client";

import { X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { formatAppointmentDateTime } from "@/lib/date-format";
import { formatPredictionResult } from "@/lib/prediction-format";

interface ImagePreviewPrediction {
  id?: number;
  resultado: string;
  confianza: number;
  imagen?: string | null;
}

interface ImagePreviewDialogProps {
  preview: {
    prediction: ImagePreviewPrediction;
    imageUrl: string;
    appointmentDate?: string;
  } | null;
  onClose: () => void;
}

export function ImagePreviewDialog({ preview, onClose }: ImagePreviewDialogProps) {
  if (!preview) {
    return null;
  }

  const confidence = Math.round(preview.prediction.confianza * 100);
  const resultLabel = formatPredictionResult(preview.prediction.resultado);
  const dateLabel = preview.appointmentDate
    ? formatAppointmentDateTime(preview.appointmentDate).label
    : "Fecha no disponible";

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/95 p-4 text-white">
      <div className="mx-auto flex h-full max-w-6xl flex-col">
        <div className="flex items-start justify-between gap-4 py-3">
          <div>
            <p className="text-sm text-slate-300">Visor dermatologico IA</p>
            <h2 className="text-xl font-semibold">{resultLabel}</h2>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            aria-label="Cerrar imagen"
            className="text-white hover:bg-white/10 hover:text-white"
          >
            <X />
          </Button>
        </div>

        <div className="grid min-h-0 flex-1 gap-4 lg:grid-cols-[1fr_280px]">
          <div className="flex min-h-[360px] items-center justify-center rounded-lg border border-white/10 bg-black/40 p-3 md:p-6">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={preview.imageUrl}
              alt=""
              className="max-h-[72vh] w-auto max-w-full rounded-md object-contain shadow-2xl"
            />
          </div>

          <aside className="rounded-lg border border-white/10 bg-white/10 p-4 backdrop-blur">
            <div className="space-y-4">
              <div>
                <p className="text-xs font-medium uppercase text-slate-300">Resultado IA</p>
                <p className="mt-1 text-lg font-semibold">{resultLabel}</p>
              </div>
              <div>
                <p className="text-xs font-medium uppercase text-slate-300">Confianza</p>
                <p className="mt-1 text-lg font-semibold">{confidence}%</p>
              </div>
              <div>
                <p className="text-xs font-medium uppercase text-slate-300">Fecha cita</p>
                <p className="mt-1 text-sm text-slate-100">{dateLabel}</p>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}
