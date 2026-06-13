"use client";

import { useState } from "react";
import { AlertCircle, Plus, RefreshCw, Search, Stethoscope, Users } from "lucide-react";

import { DoctorDetails } from "@/components/doctors/doctor-details";
import { DoctorRegisterDialog } from "@/components/doctors/doctor-register-dialog";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useDoctorsAdmin } from "@/hooks/use-doctors-admin";

export default function DoctoresPage() {
  const {
    doctors,
    selectedDoctor,
    selectedStats,
    selectedActivity,
    isLoadingDoctors,
    isLoadingDetails,
    error,
    reload,
    reloadDoctorsOnly,
    selectDoctor
  } = useDoctorsAdmin();

  const [searchTerm, setSearchTerm] = useState("");
  const [isRegisterOpen, setIsRegisterOpen] = useState(false);

  // Filtrado de doctores en base a la barra de búsqueda
  const filteredDoctors = doctors.filter((doc) =>
    doc.nombre.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Clases y colores de disponibilidad para el listado lateral
  const dotColors = {
    alta: "bg-emerald-500",
    media: "bg-amber-500",
    "alta carga": "bg-rose-500"
  };

  const availabilityBorder = {
    alta: "border-emerald-100 hover:border-emerald-300",
    media: "border-amber-100 hover:border-amber-300",
    "alta carga": "border-rose-100 hover:border-rose-300"
  };

  const getSexoInitial = (sexo: string | null) => {
    if (!sexo) return "-";
    const s = sexo.trim().toLowerCase();
    if (s === "masculino") return "M";
    if (s === "femenino") return "F";
    return sexo.substring(0, 1).toUpperCase();
  };

  return (
    <>
      <div className="grid gap-6 xl:grid-cols-[380px_1fr]">
        
        {/* LADO IZQUIERDO: Listado de Doctores */}
        <Card className="h-fit shadow-sm border">
          <CardHeader className="space-y-4 pb-4">
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-lg font-bold text-slate-800 flex items-center gap-2">
                  <Stethoscope className="h-5 w-5 text-slate-700" />
                  Médicos
                </CardTitle>
                <CardDescription className="text-xs">
                  Carga laboral y registro de personal.
                </CardDescription>
              </div>
              <Button
                size="sm"
                onClick={() => setIsRegisterOpen(true)}
                className="gap-1.5 text-xs px-2.5 h-8 bg-slate-900 text-white hover:bg-slate-800"
              >
                <Plus className="h-3.5 w-3.5" />
                Registrar
              </Button>
            </div>

            {/* Buscador e Indicador de recarga */}
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-slate-400" />
                <Input
                  placeholder="Buscar doctor..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-8 text-xs h-9 bg-slate-50/50 focus:bg-white"
                />
              </div>
              <Button
                variant="outline"
                size="icon"
                onClick={() => void reload()}
                disabled={isLoadingDoctors}
                className="h-9 w-9"
                title="Actualizar listado"
              >
                <RefreshCw className={`h-4 w-4 text-slate-500 ${isLoadingDoctors ? "animate-spin" : ""}`} />
              </Button>
            </div>
          </CardHeader>

          <CardContent className="pt-2">
            {error ? (
              <div className="mb-4 flex items-start gap-2.5 rounded-lg border border-red-200 bg-red-50 px-3.5 py-3 text-xs text-red-700">
                <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
                <div>{error}</div>
              </div>
            ) : null}

            {isLoadingDoctors ? (
              <div className="grid gap-2.5">
                {Array.from({ length: 5 }).map((_, index) => (
                  <div key={index} className="h-16 animate-pulse rounded-lg bg-slate-100" />
                ))}
              </div>
            ) : filteredDoctors.length === 0 ? (
              <div className="text-center py-10 text-slate-400">
                <Users className="mx-auto h-8 w-8 text-slate-300 mb-2" />
                <p className="text-xs">No se encontraron doctores.</p>
              </div>
            ) : (
              <div className="grid gap-2.5 max-h-[500px] overflow-y-auto pr-1">
                {filteredDoctors.map((doc) => {
                  const isSelected = selectedDoctor?.id === doc.id;
                  return (
                    <button
                      key={doc.id}
                      onClick={() => selectDoctor(doc.id)}
                      className={`text-left w-full rounded-lg border p-3 transition-all ${
                        isSelected
                          ? "bg-slate-900 border-slate-900 text-white shadow-md shadow-slate-900/10"
                          : `bg-slate-50/50 hover:bg-slate-100/50 text-slate-800 ${availabilityBorder[doc.disponibilidad]}`
                      }`}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="min-w-0">
                          <h4 className="font-semibold text-xs truncate leading-snug">
                            {doc.nombre}
                          </h4>
                          <p className={`text-[10px] mt-0.5 ${isSelected ? "text-slate-300" : "text-slate-400"}`}>
                            Sexo: {getSexoInitial(doc.sexo)} • {doc.edad ?? "N/A"} años
                          </p>
                        </div>
                        {/* Indicador de disponibilidad */}
                        <span
                          className={`h-2.5 w-2.5 rounded-full shrink-0 mt-0.5 ${dotColors[doc.disponibilidad]}`}
                          title={`Disponibilidad ${doc.disponibilidad}`}
                        />
                      </div>

                      <div className="mt-3 flex items-center justify-end border-t border-dotted border-current/20 pt-2 text-[10px]">
                        <span className={isSelected ? "text-slate-300" : "text-slate-500"}>
                          Confirmadas: <strong className="font-bold">{doc.citas_confirmadas}</strong>
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>

        {/* LADO DERECHO: Detalle expandido del Doctor */}
        <div className="min-w-0">
          <DoctorDetails
            doctor={selectedDoctor}
            stats={selectedStats}
            activity={selectedActivity}
            isLoading={isLoadingDetails}
          />
        </div>

      </div>

      {/* Modal de Registro de Doctor */}
      <DoctorRegisterDialog
        isOpen={isRegisterOpen}
        onClose={() => setIsRegisterOpen(false)}
        onSuccess={() => {
          setIsRegisterOpen(false);
          void reloadDoctorsOnly(); // Refrescar solo el listado para mantener al doctor actual si se desea
        }}
      />
    </>
  );
}
