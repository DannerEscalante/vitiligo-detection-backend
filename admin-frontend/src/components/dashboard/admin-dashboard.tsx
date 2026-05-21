"use client";

import { AlertCircle, RefreshCw } from "lucide-react";

import { AppointmentsStatusCard } from "@/components/dashboard/appointments-status-card";
import { BarReportCard } from "@/components/dashboard/bar-report-card";
import { KpiCards } from "@/components/dashboard/kpi-cards";
import { RecentActivityCard } from "@/components/dashboard/recent-activity-card";
import { Button } from "@/components/ui/button";
import { useAdminDashboard } from "@/hooks/use-admin-dashboard";

export function AdminDashboard() {
  const {
    patients,
    doctors,
    mostUsedTreatments,
    mostContinuedTreatments,
    appointmentStatusCounts,
    recentAppointments,
    isLoading,
    error,
    reload
  } = useAdminDashboard();

  const totalTreatmentsRegistered = mostUsedTreatments.reduce(
    (sum, treatment) => sum + treatment.cantidad,
    0
  );

  if (isLoading) {
    return (
      <div className="grid gap-4">
        {Array.from({ length: 8 }).map((_, index) => (
          <div key={index} className="h-24 animate-pulse rounded-md bg-muted" />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold">Resumen administrativo</h1>
          <p className="text-sm text-muted-foreground">
            Indicadores operativos basados en registros reales del sistema.
          </p>
        </div>
        <Button variant="outline" onClick={() => void reload()}>
          <RefreshCw />
          Actualizar
        </Button>
      </div>

      {error ? (
        <div className="flex items-start gap-3 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
          <p>{error}</p>
        </div>
      ) : null}

      <KpiCards
        pendingAppointments={appointmentStatusCounts.pendiente}
        totalPatients={patients.length}
        totalDoctors={doctors.length}
        totalTreatmentsRegistered={totalTreatmentsRegistered}
      />

      <section className="grid gap-6 xl:grid-cols-[1fr_0.85fr]">
        <BarReportCard
          title="Tratamientos mas usados"
          description="Cantidad de tratamientos registrados por tipo."
          emptyText="No hay tratamientos registrados."
          rows={mostUsedTreatments.map((item) => ({
            label: item.tipo_tratamiento,
            value: item.cantidad
          }))}
        />
        <AppointmentsStatusCard counts={appointmentStatusCounts} />
      </section>

      <section className="grid gap-6 xl:grid-cols-[1fr_0.85fr]">
        <RecentActivityCard appointments={recentAppointments} />
        <BarReportCard
          title="Tratamientos mas continuados"
          description="Continuidad terapeutica por reutilizacion del mismo tratamiento en historiales consecutivos."
          emptyText="No hay continuidades terapeuticas registradas."
          rows={mostContinuedTreatments.map((item) => ({
            label: item.tipo_tratamiento,
            value: item.continuaciones
          }))}
        />
      </section>

      <p className="text-xs text-muted-foreground">
        No se muestran metricas de efectividad clinica ni interpretaciones IA automaticas.
      </p>
    </div>
  );
}
