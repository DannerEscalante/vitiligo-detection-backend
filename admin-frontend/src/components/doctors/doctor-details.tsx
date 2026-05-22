"use client";

import { useState } from "react";
import { 
  Activity, 
  Calendar, 
  ClipboardList, 
  FileText, 
  Mail, 
  Percent, 
  Stethoscope, 
  User, 
  Users 
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { formatAppointmentDateTime } from "@/lib/date-format";
import type { DoctorAdminSummary, DoctorRecentActivity, DoctorStats } from "@/types/doctors";

interface DoctorDetailsProps {
  doctor: DoctorAdminSummary | null;
  stats: DoctorStats | null;
  activity: DoctorRecentActivity | null;
  isLoading: boolean;
}

export function DoctorDetails({ doctor, stats, activity, isLoading }: DoctorDetailsProps) {
  const [activeTab, setActiveTab] = useState<"citas" | "pacientes" | "historiales">("citas");

  if (!doctor) {
    return (
      <Card className="flex h-[450px] items-center justify-center border-dashed">
        <div className="text-center text-muted-foreground">
          <Stethoscope className="mx-auto h-12 w-12 text-slate-300 animate-pulse" />
          <h3 className="mt-4 text-lg font-medium text-slate-800">Ningún doctor seleccionado</h3>
          <p className="mt-1 text-sm text-slate-400 max-w-xs">
            Selecciona un médico del listado de la izquierda para ver su carga laboral, estadísticas y actividad reciente.
          </p>
        </div>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        {/* Cabecera esqueleto */}
        <Card className="animate-pulse">
          <CardContent className="h-28" />
        </Card>
        {/* Grid de estadísticas esqueleto */}
        <div className="grid gap-4 md:grid-cols-2">
          <Card className="h-32 animate-pulse" />
          <Card className="h-32 animate-pulse" />
        </div>
        {/* Sección de detalles esqueleto */}
        <Card className="h-64 animate-pulse" />
      </div>
    );
  }

  // Clases y colores de disponibilidad
  const availabilityColors = {
    alta: "bg-emerald-50 text-emerald-700 border-emerald-200",
    media: "bg-amber-50 text-amber-700 border-amber-200",
    "alta carga": "bg-rose-50 text-rose-700 border-rose-200"
  };

  const availabilityLabels = {
    alta: "Disponible (Alta)",
    media: "Moderada (Media)",
    "alta carga": "Alta Carga Médica"
  };

  const getSexoLabel = (sexo: string | null) => {
    if (!sexo) return "No especificado";
    const s = sexo.trim().toLowerCase();
    if (s === "masculino") return "Masculino";
    if (s === "femenino") return "Femenino";
    return sexo;
  };

  // Desglose de estados de citas para porcentajes
  const totalCitas = stats?.total_citas ?? 0;
  const dist = stats?.distribucion_estados ?? { pendiente: 0, confirmada: 0, cancelada: 0, finalizada: 0 };
  
  const getPercent = (count: number) => {
    if (totalCitas === 0) return 0;
    return Math.round((count / totalCitas) * 100);
  };

  return (
    <div className="space-y-6">
      {/* 1. Datos Básicos Header */}
      <Card className="overflow-hidden border bg-gradient-to-r from-slate-50 to-white shadow-sm">
        <CardContent className="p-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-4">
              <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-slate-900 text-white shadow-md">
                <Stethoscope className="h-7 w-7" />
              </div>
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <h2 className="text-xl font-bold text-slate-800">{doctor.nombre}</h2>
                  <Badge variant="outline" className={`font-semibold capitalize px-2 py-0.5 border ${availabilityColors[doctor.disponibilidad]}`}>
                    {availabilityLabels[doctor.disponibilidad]}
                  </Badge>
                </div>
                <div className="mt-1.5 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-slate-500">
                  <span className="flex items-center gap-1.5">
                    <Mail className="h-4 w-4" />
                    {stats?.datos_basicos.email ?? "Sin correo"}
                  </span>
                  <span className="hidden sm:inline text-slate-300">•</span>
                  <span className="flex items-center gap-1.5">
                    <User className="h-4 w-4" />
                    {getSexoLabel(doctor.sexo)}, {doctor.edad ?? "N/A"} años
                  </span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 2. Tarjetas de Resumen Numérico */}
      <div className="grid gap-4 sm:grid-cols-2">
        <Card className="border bg-white shadow-sm hover:shadow transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Total Citas Gestionadas
            </CardTitle>
            <Calendar className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-extrabold text-slate-800">{stats?.total_citas ?? 0}</div>
            <p className="mt-1 text-xs text-slate-500">Historial completo asignado en la clínica.</p>
          </CardContent>
        </Card>

        <Card className="border bg-white shadow-sm hover:shadow transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Pacientes Únicos Atendidos
            </CardTitle>
            <Users className="h-4 w-4 text-indigo-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-extrabold text-slate-800">{stats?.pacientes_unicos ?? 0}</div>
            <p className="mt-1 text-xs text-slate-500">Pacientes con citas confirmadas o historial.</p>
          </CardContent>
        </Card>
      </div>

      {/* 3. Distribución de Estados & Tratamientos Aplicados (Split Layout de Widgets) */}
      <div className="grid gap-6 lg:grid-cols-2">
        
        {/* Distribución de Estados de Citas */}
        <Card className="border bg-white shadow-sm">
          <CardHeader>
            <CardTitle className="text-sm font-semibold flex items-center gap-2 text-slate-800">
              <Percent className="h-4 w-4 text-slate-500" />
              Distribución de Estados
            </CardTitle>
            <CardDescription>Análisis porcentual de citas asignadas.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {totalCitas === 0 ? (
              <div className="text-center py-6 text-sm text-slate-400">
                No hay citas registradas para este médico.
              </div>
            ) : (
              <>
                {/* Finalizadas */}
                <div className="space-y-1">
                  <div className="flex justify-between text-xs font-medium text-slate-700">
                    <span>Finalizadas ({dist.finalizada})</span>
                    <span>{getPercent(dist.finalizada)}%</span>
                  </div>
                  <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
                    <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${getPercent(dist.finalizada)}%` }} />
                  </div>
                </div>

                {/* Confirmadas */}
                <div className="space-y-1">
                  <div className="flex justify-between text-xs font-medium text-slate-700">
                    <span>Confirmadas ({dist.confirmada})</span>
                    <span>{getPercent(dist.confirmada)}%</span>
                  </div>
                  <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
                    <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${getPercent(dist.confirmada)}%` }} />
                  </div>
                </div>

                {/* Pendientes */}
                <div className="space-y-1">
                  <div className="flex justify-between text-xs font-medium text-slate-700">
                    <span>Pendientes ({dist.pendiente})</span>
                    <span>{getPercent(dist.pendiente)}%</span>
                  </div>
                  <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
                    <div className="h-full bg-blue-500 rounded-full" style={{ width: `${getPercent(dist.pendiente)}%` }} />
                  </div>
                </div>

                {/* Canceladas */}
                <div className="space-y-1">
                  <div className="flex justify-between text-xs font-medium text-slate-700">
                    <span>Canceladas ({dist.cancelada})</span>
                    <span>{getPercent(dist.cancelada)}%</span>
                  </div>
                  <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
                    <div className="h-full bg-rose-500 rounded-full" style={{ width: `${getPercent(dist.cancelada)}%` }} />
                  </div>
                </div>
              </>
            )}
          </CardContent>
        </Card>

        {/* Tratamientos Aplicados */}
        <Card className="border bg-white shadow-sm">
          <CardHeader>
            <CardTitle className="text-sm font-semibold flex items-center gap-2 text-slate-800">
              <ClipboardList className="h-4 w-4 text-slate-500" />
              Tratamientos Iniciados
            </CardTitle>
            <CardDescription>Prescripciones clínicas aplicadas por el médico.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="max-h-[220px] overflow-y-auto space-y-3 pr-1">
              {!stats?.tratamientos_aplicados || stats.tratamientos_aplicados.length === 0 ? (
                <div className="text-center py-6 text-sm text-slate-400">
                  Ningún tratamiento prescrito por el momento.
                </div>
              ) : (
                stats.tratamientos_aplicados.map((tr) => (
                  <div key={tr.id} className="rounded-lg border border-slate-100 bg-slate-50 p-3 space-y-1.5 text-xs">
                    <div className="flex items-center justify-between font-semibold">
                      <span className="text-slate-800 text-sm">{tr.tipo_tratamiento}</span>
                      <Badge variant="outline" className={`text-[10px] font-bold ${
                        tr.estado === "activo" 
                          ? "bg-emerald-50 text-emerald-700 border-emerald-200" 
                          : "bg-slate-100 text-slate-500"
                      }`}>
                        {tr.estado}
                      </Badge>
                    </div>
                    <div className="flex justify-between text-[11px] text-slate-400">
                      <span>Paciente: {tr.paciente_nombre}</span>
                      <span>
                        {tr.fecha_inicio 
                          ? new Date(tr.fecha_inicio).toLocaleDateString("es-ES") 
                          : "Sin fecha"}
                      </span>
                    </div>
                    {tr.notas && (
                      <p className="text-slate-500 italic mt-1 border-t border-slate-200/60 pt-1 text-[11px]">
                        &quot;{tr.notas}&quot;
                      </p>
                    )}
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>

      </div>

      {/* 4. Línea de Tiempo de Actividad Reciente */}
      <Card className="border bg-white shadow-sm">
        <CardHeader className="pb-3 border-b">
          <CardTitle className="text-sm font-semibold flex items-center gap-2 text-slate-800">
            <Activity className="h-4 w-4 text-slate-500" />
            Registro de Actividad Reciente
          </CardTitle>
          <CardDescription>Monitoreo en tiempo real de la actividad clínica.</CardDescription>
          
          {/* Pestanas de Actividad */}
          <div className="mt-4 flex gap-1 rounded-lg bg-slate-100 p-1 text-xs">
            <button
              onClick={() => setActiveTab("citas")}
              className={`flex-1 rounded-md py-1.5 font-medium transition-colors ${
                activeTab === "citas" ? "bg-white text-slate-800 shadow" : "text-slate-500 hover:text-slate-700"
              }`}
            >
              Últimas Citas
            </button>
            <button
              onClick={() => setActiveTab("pacientes")}
              className={`flex-1 rounded-md py-1.5 font-medium transition-colors ${
                activeTab === "pacientes" ? "bg-white text-slate-800 shadow" : "text-slate-500 hover:text-slate-700"
              }`}
            >
              Últimos Pacientes
            </button>
            <button
              onClick={() => setActiveTab("historiales")}
              className={`flex-1 rounded-md py-1.5 font-medium transition-colors ${
                activeTab === "historiales" ? "bg-white text-slate-800 shadow" : "text-slate-500 hover:text-slate-700"
              }`}
            >
              Últimos Historiales
            </button>
          </div>
        </CardHeader>

        <CardContent className="pt-4">
          <div className="min-h-[220px]">
            {/* TAB CITAS */}
            {activeTab === "citas" && (
              <div className="space-y-4">
                {!activity?.ultimas_citas || activity.ultimas_citas.length === 0 ? (
                  <p className="text-center py-8 text-sm text-slate-400">Sin citas recientes registradas.</p>
                ) : (
                  <div className="relative border-l border-slate-100 pl-4 space-y-4">
                    {activity.ultimas_citas.map((cita) => {
                      const dt = cita.fecha_hora ? formatAppointmentDateTime(cita.fecha_hora) : null;
                      return (
                        <div key={cita.id} className="relative">
                          {/* Nodo de timeline */}
                          <div className="absolute -left-[21px] top-1.5 flex h-3.5 w-3.5 items-center justify-center rounded-full bg-white border border-slate-300">
                            <div className="h-1.5 w-1.5 rounded-full bg-slate-500" />
                          </div>
                          <div>
                            <div className="flex items-center justify-between text-xs">
                              <span className="font-semibold text-slate-800">
                                Cita con {cita.paciente_nombre}
                              </span>
                              <Badge className={`text-[10px] uppercase font-bold py-0 ${
                                cita.estado === "finalizada" 
                                  ? "bg-emerald-50 text-emerald-700 border-emerald-200 border" 
                                  : cita.estado === "confirmada" 
                                  ? "bg-indigo-50 text-indigo-700 border border-indigo-200" 
                                  : cita.estado === "cancelada"
                                  ? "bg-rose-50 text-rose-700 border border-rose-200"
                                  : "bg-blue-50 text-blue-700 border border-blue-200"
                              }`}>
                                {cita.estado}
                              </Badge>
                            </div>
                            <p className="text-[11px] text-slate-400 mt-0.5">
                              {dt ? `${dt.label} - ID #${cita.id}` : "Fecha no disponible"}
                            </p>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            )}

            {/* TAB PACIENTES */}
            {activeTab === "pacientes" && (
              <div className="grid gap-3 sm:grid-cols-2">
                {!activity?.ultimos_pacientes || activity.ultimos_pacientes.length === 0 ? (
                  <p className="col-span-2 text-center py-8 text-sm text-slate-400">Sin pacientes recientes atendidos.</p>
                ) : (
                  activity.ultimos_pacientes.map((pac) => (
                    <div key={pac.id} className="flex items-center gap-3 rounded-lg border border-slate-100 p-3 bg-slate-50/60">
                      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600">
                        <User className="h-4 w-4" />
                      </div>
                      <div className="min-w-0">
                        <p className="text-xs font-semibold text-slate-800 truncate">{pac.nombre}</p>
                        <p className="text-[10px] text-slate-500">
                          {getSexoLabel(pac.sexo)}, {pac.edad ?? "N/A"} años
                        </p>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}

            {/* TAB HISTORIALES */}
            {activeTab === "historiales" && (
              <div className="space-y-4">
                {!activity?.ultimos_historiales || activity.ultimos_historiales.length === 0 ? (
                  <p className="text-center py-8 text-sm text-slate-400">Sin historiales clínicos recientes creados.</p>
                ) : (
                  <div className="space-y-3">
                    {activity.ultimos_historiales.map((h) => {
                      const fechaFormat = h.fecha 
                        ? new Date(h.fecha).toLocaleDateString("es-ES", {
                            day: "numeric",
                            month: "short",
                            hour: "2-digit",
                            minute: "2-digit"
                          })
                        : "Fecha no disponible";
                      return (
                        <div key={h.id} className="rounded-lg border border-slate-100 p-3 space-y-2 bg-slate-50/40">
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-semibold text-slate-700 flex items-center gap-1.5">
                              <FileText className="h-3.5 w-3.5 text-slate-400" />
                              Paciente: {h.paciente_nombre}
                            </span>
                            <span className="text-[10px] text-slate-400">{fechaFormat}</span>
                          </div>
                          <div className="text-xs text-slate-600 bg-white rounded border p-2 italic leading-relaxed">
                            &quot;{h.diagnostico}&quot;
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            )}
          </div>
        </CardContent>
      </Card>

    </div>
  );
}
