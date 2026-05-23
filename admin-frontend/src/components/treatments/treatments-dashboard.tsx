"use client";

import { useState } from "react";
import { AlertCircle, RefreshCw } from "lucide-react";

import { TreatmentCreatePanel } from "@/components/treatments/treatment-create-panel";
import { TreatmentDetails } from "@/components/treatments/treatment-details";
import { TreatmentsList } from "@/components/treatments/treatments-list";
import { Button } from "@/components/ui/button";
import { useTreatmentsAdmin } from "@/hooks/use-treatments-admin";

export function TreatmentsDashboard() {
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const {
    treatments,
    selectedTreatment,
    selectedStats,
    isLoadingList,
    isLoadingStats,
    error,
    selectTreatment,
    reloadList,
    reloadSelectedStats
  } = useTreatmentsAdmin();

  async function handleUpdated() {
    await reloadList();
    await reloadSelectedStats();
  }

  async function handleCreated() {
    await reloadList();
  }

  return (
    <>
      <div className="space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold">Tratamientos</h1>
            <p className="text-sm text-muted-foreground">
              Catalogo administrativo y estadisticas reales de uso clinico.
            </p>
          </div>
          <Button variant="outline" onClick={() => void reloadList()} disabled={isLoadingList}>
            <RefreshCw className={isLoadingList ? "animate-spin" : ""} />
            Actualizar
          </Button>
        </div>

        {error ? (
          <div className="flex items-start gap-3 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
            <p>{error}</p>
          </div>
        ) : null}

        <div className="grid gap-6 xl:grid-cols-[380px_1fr]">
          {isLoadingList ? (
            <div className="grid gap-3">
              {Array.from({ length: 6 }).map((_, index) => (
                <div key={index} className="h-20 animate-pulse rounded-md bg-muted" />
              ))}
            </div>
          ) : (
            <TreatmentsList
              treatments={treatments}
              selectedId={selectedTreatment?.id ?? null}
              onSelect={selectTreatment}
              onCreate={() => setIsCreateOpen(true)}
            />
          )}

          <TreatmentDetails
            treatment={selectedTreatment}
            stats={selectedStats}
            isLoading={isLoadingStats}
            onUpdated={() => void handleUpdated()}
          />
        </div>
      </div>

      <TreatmentCreatePanel
        isOpen={isCreateOpen}
        onClose={() => setIsCreateOpen(false)}
        onCreated={() => void handleCreated()}
      />
    </>
  );
}
