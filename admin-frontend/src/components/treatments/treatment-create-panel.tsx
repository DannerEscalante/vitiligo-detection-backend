"use client";

import { FormEvent, useState } from "react";
import { X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { createTreatmentTypeAdmin } from "@/lib/treatments-api";

interface TreatmentCreatePanelProps {
  isOpen: boolean;
  onClose: () => void;
  onCreated: () => void;
}

export function TreatmentCreatePanel({
  isOpen,
  onClose,
  onCreated
}: TreatmentCreatePanelProps) {
  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) {
    return null;
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!nombre.trim()) {
      setError("El nombre es obligatorio.");
      return;
    }

    setIsSaving(true);
    setError(null);

    try {
      await createTreatmentTypeAdmin({
        nombre: nombre.trim(),
        descripcion: descripcion.trim() || undefined
      });
      setNombre("");
      setDescripcion("");
      onCreated();
      onClose();
    } catch (createError) {
      setError(createError instanceof Error ? createError.message : "No se pudo crear.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/45 p-4">
      <Card className="w-full max-w-lg">
        <CardHeader className="flex flex-row items-start justify-between space-y-0">
          <div>
            <CardTitle>Nuevo tratamiento</CardTitle>
            <CardDescription>Registra un tipo de tratamiento del catalogo clinico.</CardDescription>
          </div>
          <Button variant="ghost" size="icon" onClick={onClose} aria-label="Cerrar">
            <X />
          </Button>
        </CardHeader>
        <CardContent>
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="space-y-2">
              <Label htmlFor="nombre-tratamiento">Nombre</Label>
              <Input
                id="nombre-tratamiento"
                value={nombre}
                onChange={(event) => setNombre(event.target.value)}
                placeholder="Fototerapia"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="descripcion-tratamiento">Descripcion</Label>
              <textarea
                id="descripcion-tratamiento"
                value={descripcion}
                onChange={(event) => setDescripcion(event.target.value)}
                rows={4}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-ring"
                placeholder="Descripcion clinica general del tratamiento"
              />
            </div>
            {error ? (
              <p className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
                {error}
              </p>
            ) : null}
            <div className="flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={onClose} disabled={isSaving}>
                Cancelar
              </Button>
              <Button type="submit" disabled={isSaving}>
                {isSaving ? "Guardando..." : "Crear tratamiento"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
