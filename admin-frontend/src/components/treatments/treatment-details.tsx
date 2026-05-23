"use client";

import { useState } from "react";
import {
  Activity,
  Calendar,
  ClipboardList,
  Edit2,
  Stethoscope,
  Users,
  X,
  type LucideIcon
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { updateTreatmentType } from "@/lib/treatments-api";
import type { TreatmentTypeAdmin, TreatmentTypeStats } from "@/types/treatments";

interface TreatmentDetailsProps {
  treatment: TreatmentTypeAdmin | null;
  stats: TreatmentTypeStats | null;
  isLoading: boolean;
  onUpdated: () => void;
}

function estadoBadgeClass(estado: string) {
  if (estado === "activo") return "border-emerald-200 bg-emerald-50 text-emerald-700";
  if (estado === "finalizado") return "border-slate-200 bg-slate-100 text-slate-600";
  return "border-amber-200 bg-amber-50 text-amber-700";
}

function formatDate(value: string | null) {
  if (!value) return "Sin fecha";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Sin fecha";
  return date.toLocaleDateString("es-ES", {
    day: "2-digit",
    month: "short",
    year: "numeric"
  });
}

export function TreatmentDetails({ treatment, stats, isLoading, onUpdated }: TreatmentDetailsProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editNombre, setEditNombre] = useState("");
  const [editDescripcion, setEditDescripcion] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [editError, setEditError] = useState<string | null>(null);

  function openEdit() {
    if (!treatment) return;
    setEditNombre(treatment.nombre);
    setEditDescripcion(treatment.descripcion ?? "");
    setEditError(null);
    setIsEditing(true);
  }

  async function handleSave() {
    if (!treatment) return;
    if (!editNombre.trim()) {
      setEditError("El nombre es obligatorio.");
      return;
    }

    setIsSaving(true);
    setEditError(null);

    try {
      await updateTreatmentType(treatment.id, {
        nombre: editNombre.trim(),
        descripcion: editDescripcion.trim()
      });
      setIsEditing(false);
      onUpdated();
    } catch (error) {
      setEditError(error instanceof Error ? error.message : "No se pudo guardar.");
    } finally {
      setIsSaving(false);
    }
  }

  if (!treatment) {
    return (
      <Card className="flex min-h-[520px] items-center justify-center border-dashed">
        <div className="max-w-sm text-center text-muted-foreground">
          <ClipboardList className="mx-auto h-12 w-12 text-muted-foreground" />
          <h3 className="mt-4 text-lg font-medium text-foreground">Ningun tratamiento seleccionado</h3>
          <p className="mt-1 text-sm">
            Selecciona un tipo de tratamiento para ver estadisticas y actividad reciente.
          </p>
        </div>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Card className="h-32 animate-pulse" />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          {Array.from({ length: 5 }).map((_, index) => (
            <Card key={index} className="h-24 animate-pulse" />
          ))}
        </div>
        <Card className="h-72 animate-pulse" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardContent className="p-6">
          {isEditing ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between gap-3">
                <h2 className="text-base font-semibold">Editar tratamiento</h2>
                <Button variant="ghost" size="icon" onClick={() => setIsEditing(false)}>
                  <X />
                </Button>
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit-treatment-name">Nombre</Label>
                <Input
                  id="edit-treatment-name"
                  value={editNombre}
                  onChange={(event) => setEditNombre(event.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit-treatment-description">Descripcion</Label>
                <textarea
                  id="edit-treatment-description"
                  value={editDescripcion}
                  onChange={(event) => setEditDescripcion(event.target.value)}
                  rows={4}
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
              {editError ? (
                <p className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
                  {editError}
                </p>
              ) : null}
              <div className="flex justify-end gap-2">
                <Button variant="outline" onClick={() => setIsEditing(false)} disabled={isSaving}>
                  Cancelar
                </Button>
                <Button onClick={() => void handleSave()} disabled={isSaving}>
                  {isSaving ? "Guardando..." : "Guardar cambios"}
                </Button>
              </div>
            </div>
          ) : (
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div className="flex items-start gap-4">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-md bg-primary text-primary-foreground">
                  <ClipboardList className="h-6 w-6" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold">{treatment.nombre}</h2>
                  <p className="mt-1 max-w-2xl text-sm text-muted-foreground">
                    {treatment.descripcion ?? "Sin descripcion registrada."}
                  </p>
                </div>
              </div>
              <Button variant="outline" size="sm" onClick={openEdit}>
                <Edit2 />
                Editar
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
        <MetricCard title="Total usos" value={stats?.total_usos ?? 0} icon={Activity} />
        <MetricCard title="Activos" value={stats?.activos ?? 0} icon={Activity} tone="teal" />
        <MetricCard title="Continuidad" value={stats?.continuaciones ?? 0} icon={ClipboardList} tone="teal" />
        <MetricCard title="Pacientes" value={stats?.pacientes_unicos ?? 0} icon={Users} />
        <MetricCard title="Doctores" value={stats?.doctores_unicos ?? 0} icon={Stethoscope} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <RelatedList
          title="Pacientes relacionados"
          description="Pacientes con registros asociados a este tratamiento."
          emptyText="Sin pacientes relacionados."
          rows={stats?.pacientes_relacionados ?? []}
        />
        <RelatedList
          title="Doctores relacionados"
          description="Doctores con prescripciones asociadas a este tratamiento."
          emptyText="Sin doctores relacionados."
          rows={stats?.doctores_relacionados ?? []}
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <RelatedList
          title="Doctores que mas lo aplicaron"
          description="Top 5 por numero de prescripciones."
          emptyText="Sin datos de prescriptores."
          rows={stats?.top_doctores ?? []}
        />
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-sm">
              <Calendar className="h-4 w-4" />
              Actividad reciente
            </CardTitle>
            <CardDescription>Ultimos usos registrados para este tratamiento.</CardDescription>
          </CardHeader>
          <CardContent>
            {!stats?.ultimos_usos || stats.ultimos_usos.length === 0 ? (
              <div className="rounded-md border border-dashed p-5 text-sm text-muted-foreground">
                Sin actividad registrada.
              </div>
            ) : (
              <div className="space-y-3">
                {stats.ultimos_usos.map((uso) => (
                  <div key={uso.id} className="rounded-md border bg-white p-3">
                    <div className="flex items-center justify-between gap-3">
                      <p className="text-sm font-medium">{uso.paciente_nombre}</p>
                      <Badge variant="outline" className={estadoBadgeClass(uso.estado)}>
                        {uso.estado}
                      </Badge>
                    </div>
                    <p className="mt-1 text-xs text-muted-foreground">
                      Dr. {uso.doctor_nombre} · {formatDate(uso.fecha_inicio)}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function MetricCard({
  title,
  value,
  icon: Icon,
  tone = "default"
}: {
  title: string;
  value: number;
  icon: LucideIcon;
  tone?: "default" | "teal";
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-xs font-semibold uppercase text-muted-foreground">{title}</CardTitle>
        <Icon className={tone === "teal" ? "h-4 w-4 text-teal-600" : "h-4 w-4 text-muted-foreground"} />
      </CardHeader>
      <CardContent>
        <div className={tone === "teal" ? "text-3xl font-semibold text-teal-700" : "text-3xl font-semibold"}>
          {value}
        </div>
      </CardContent>
    </Card>
  );
}

function RelatedList({
  title,
  description,
  emptyText,
  rows
}: {
  title: string;
  description: string;
  emptyText: string;
  rows: Array<{ nombre: string; usos: number }>;
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm">{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        {rows.length === 0 ? (
          <div className="rounded-md border border-dashed p-5 text-sm text-muted-foreground">
            {emptyText}
          </div>
        ) : (
          <div className="space-y-3">
            {rows.map((row, index) => (
              <div
                key={`${row.nombre}-${index}`}
                className="flex items-center justify-between rounded-md border bg-muted/30 px-3 py-2 text-sm"
              >
                <span className="font-medium">{row.nombre}</span>
                <span className="text-xs text-muted-foreground">{row.usos} usos</span>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
