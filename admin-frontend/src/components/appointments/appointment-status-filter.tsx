"use client";

import type { AppointmentStatusFilter } from "@/types/appointments";
import { cn } from "@/lib/utils";

const filters: Array<{ label: string; value: AppointmentStatusFilter }> = [
  { label: "Todas", value: "todas" },
  { label: "Pendientes", value: "pendiente" },
  { label: "Confirmadas", value: "confirmada" },
  { label: "Finalizadas", value: "finalizada" },
  { label: "Canceladas", value: "cancelada" }
];

interface AppointmentStatusFilterProps {
  selectedStatus: AppointmentStatusFilter;
  counts: Record<AppointmentStatusFilter, number>;
  onChange: (status: AppointmentStatusFilter) => void;
}

export function AppointmentStatusFilter({
  selectedStatus,
  counts,
  onChange
}: AppointmentStatusFilterProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {filters.map((filter) => (
        <button
          key={filter.value}
          type="button"
          onClick={() => onChange(filter.value)}
          className={cn(
            "inline-flex h-9 items-center gap-2 rounded-md border px-3 text-sm font-medium transition-colors",
            selectedStatus === filter.value
              ? "border-primary bg-primary text-primary-foreground"
              : "border-input bg-white text-muted-foreground hover:bg-muted hover:text-foreground"
          )}
        >
          {filter.label}
          <span
            className={cn(
              "rounded-md px-1.5 py-0.5 text-xs",
              selectedStatus === filter.value
                ? "bg-white/20 text-primary-foreground"
                : "bg-muted text-muted-foreground"
            )}
          >
            {counts[filter.value]}
          </span>
        </button>
      ))}
    </div>
  );
}
