"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import { confirmAppointment, getAppointments } from "@/lib/appointments-api";
import { getDoctors } from "@/lib/doctors-api";
import type {
  Appointment,
  AppointmentStatusFilter,
  DoctorSummary
} from "@/types/appointments";

export function useAppointments() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [doctors, setDoctors] = useState<DoctorSummary[]>([]);
  const [selectedStatus, setSelectedStatus] = useState<AppointmentStatusFilter>("todas");
  const [selectedAppointment, setSelectedAppointment] = useState<Appointment | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isConfirming, setIsConfirming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const [appointmentsResponse, doctorsResponse] = await Promise.all([
        getAppointments(),
        getDoctors()
      ]);

      setAppointments(appointmentsResponse);
      setDoctors(doctorsResponse);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "No se pudieron cargar las citas");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadData();
  }, [loadData]);

  const filteredAppointments = useMemo(() => {
    if (selectedStatus === "todas") {
      return appointments;
    }

    return appointments.filter((appointment) => appointment.estado === selectedStatus);
  }, [appointments, selectedStatus]);

  const statusCounts = useMemo(() => {
    return appointments.reduce<Record<AppointmentStatusFilter, number>>(
      (counts, appointment) => {
        counts.todas += 1;
        counts[appointment.estado] += 1;
        return counts;
      },
      {
        todas: 0,
        pendiente: 0,
        confirmada: 0,
        finalizada: 0,
        cancelada: 0
      }
    );
  }, [appointments]);

  async function confirmSelectedAppointment(doctorId: number) {
    if (!selectedAppointment) {
      return;
    }

    setIsConfirming(true);
    setError(null);
    setSuccessMessage(null);

    try {
      await confirmAppointment(selectedAppointment.id, doctorId);
      await loadData();
      setSelectedAppointment(null);
      setSuccessMessage("Cita confirmada correctamente.");
    } catch (confirmError) {
      setError(confirmError instanceof Error ? confirmError.message : "No se pudo confirmar la cita");
    } finally {
      setIsConfirming(false);
    }
  }

  return {
    appointments,
    doctors,
    filteredAppointments,
    selectedStatus,
    selectedAppointment,
    isLoading,
    isConfirming,
    error,
    successMessage,
    statusCounts,
    setSelectedStatus,
    setSelectedAppointment,
    setSuccessMessage,
    reload: loadData,
    confirmSelectedAppointment
  };
}
