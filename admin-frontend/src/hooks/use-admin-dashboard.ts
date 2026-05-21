"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import { getAppointments } from "@/lib/appointments-api";
import { getDoctors } from "@/lib/doctors-api";
import { getPatients } from "@/lib/patients-api";
import { getMostContinuedTreatments, getMostUsedTreatments } from "@/lib/reports-api";
import type { Appointment } from "@/types/appointments";
import type { DoctorSummary } from "@/types/appointments";
import type { AdminPatient } from "@/types/patients";
import type {
  MostContinuedTreatmentReport,
  MostUsedTreatmentReport
} from "@/types/reports";

export function useAdminDashboard() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [patients, setPatients] = useState<AdminPatient[]>([]);
  const [doctors, setDoctors] = useState<DoctorSummary[]>([]);
  const [mostUsedTreatments, setMostUsedTreatments] = useState<MostUsedTreatmentReport[]>([]);
  const [mostContinuedTreatments, setMostContinuedTreatments] = useState<
    MostContinuedTreatmentReport[]
  >([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadDashboard = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const [
        appointmentsResponse,
        patientsResponse,
        doctorsResponse,
        usedTreatmentsResponse,
        continuedTreatmentsResponse
      ] = await Promise.all([
        getAppointments(),
        getPatients(),
        getDoctors(),
        getMostUsedTreatments(),
        getMostContinuedTreatments()
      ]);

      setAppointments(appointmentsResponse);
      setPatients(patientsResponse);
      setDoctors(doctorsResponse);
      setMostUsedTreatments(usedTreatmentsResponse);
      setMostContinuedTreatments(continuedTreatmentsResponse);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "No se pudo cargar el dashboard");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadDashboard();
  }, [loadDashboard]);

  const appointmentStatusCounts = useMemo(() => {
    return appointments.reduce(
      (counts, appointment) => {
        counts[appointment.estado] += 1;
        return counts;
      },
      {
        pendiente: 0,
        confirmada: 0,
        finalizada: 0,
        cancelada: 0
      }
    );
  }, [appointments]);

  const recentAppointments = useMemo(() => {
    return [...appointments]
      .sort((a, b) => new Date(b.fecha_hora).getTime() - new Date(a.fecha_hora).getTime())
      .slice(0, 6);
  }, [appointments]);

  return {
    appointments,
    patients,
    doctors,
    mostUsedTreatments,
    mostContinuedTreatments,
    appointmentStatusCounts,
    recentAppointments,
    isLoading,
    error,
    reload: loadDashboard
  };
}
