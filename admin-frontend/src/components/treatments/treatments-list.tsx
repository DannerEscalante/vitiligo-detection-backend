"use client";

import { ClipboardList, Plus } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { TreatmentTypeAdmin } from "@/types/treatments";

interface TreatmentsListProps {
  treatments: TreatmentTypeAdmin[];
  selectedId: number | null;
  onSelect: (id: number) => void;
  onCreate: () => void;
}

export function TreatmentsList({
  treatments,
  selectedId,
  onSelect,
  onCreate
}: TreatmentsListProps) {
  return (
    <Card className="h-fit">
      <CardHeader className="gap-4">
        <div className="flex items-start justify-between gap-3">
          <div>
            <CardTitle>Tratamientos</CardTitle>
            <CardDescription>Catalogo administrativo de tipos de tratamiento.</CardDescription>
          </div>
          <Button size="sm" onClick={onCreate}>
            <Plus />
            Nuevo
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {treatments.length === 0 ? (
          <div className="flex min-h-64 flex-col items-center justify-center rounded-md border border-dashed bg-white p-6 text-center">
            <ClipboardList className="h-10 w-10 text-muted-foreground" aria-hidden="true" />
            <h3 className="mt-4 text-base font-semibold">Sin tratamientos registrados</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              Crea el primer tipo de tratamiento para verlo en el catalogo.
            </p>
          </div>
        ) : (
          <div className="max-h-[70vh] overflow-y-auto rounded-md border bg-white">
            {treatments.map((treatment) => (
              <button
                key={treatment.id}
                type="button"
                onClick={() => onSelect(treatment.id)}
                className={cn(
                  "block w-full border-b px-4 py-4 text-left transition-colors last:border-b-0",
                  treatment.id === selectedId ? "bg-teal-50" : "hover:bg-muted/70"
                )}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-semibold">{treatment.nombre}</p>
                    <p className="mt-1 line-clamp-2 text-xs text-muted-foreground">
                      {treatment.descripcion ?? "Sin descripcion registrada."}
                    </p>
                  </div>
                  <Badge variant="outline" className="shrink-0">
                    {treatment.total_usos} usos
                  </Badge>
                </div>
                <div className="mt-3 grid grid-cols-3 gap-2 text-xs text-muted-foreground">
                  <span>{treatment.activos} activos</span>
                  <span>{treatment.continuaciones} cont.</span>
                  <span>{treatment.pacientes_unicos} pacientes</span>
                </div>
              </button>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
