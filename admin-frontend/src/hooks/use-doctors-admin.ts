"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import { getDoctorActivity, getDoctorsAdmin, getDoctorStats } from "@/lib/doctors-api";
import type { DoctorAdminSummary, DoctorRecentActivity, DoctorStats } from "@/types/doctors";

export function useDoctorsAdmin() {
  const [doctors, setDoctors] = useState<DoctorAdminSummary[]>([]);
  const [selectedDoctorId, setSelectedDoctorId] = useState<number | null>(null);
  
  const [selectedStats, setSelectedStats] = useState<DoctorStats | null>(null);
  const [selectedActivity, setSelectedActivity] = useState<DoctorRecentActivity | null>(null);
  
  const [isLoadingDoctors, setIsLoadingDoctors] = useState(true);
  const [isLoadingDetails, setIsLoadingDetails] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const selectedDoctor = useMemo(
    () => doctors.find((doc) => doc.id === selectedDoctorId) ?? null,
    [doctors, selectedDoctorId]
  );

  const loadDoctors = useCallback(async (selectFirst = true) => {
    setIsLoadingDoctors(true);
    setError(null);

    try {
      const response = await getDoctorsAdmin();
      setDoctors(response);

      if (selectFirst && response.length > 0 && !selectedDoctorId) {
        setSelectedDoctorId(response[0].id);
      }
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "No se pudieron cargar los doctores.");
    } finally {
      setIsLoadingDoctors(false);
    }
  }, [selectedDoctorId]);

  const loadDoctorDetails = useCallback(async (docId: number) => {
    setIsLoadingDetails(true);
    setError(null);

    try {
      const [statsRes, activityRes] = await Promise.all([
        getDoctorStats(docId),
        getDoctorActivity(docId)
      ]);

      setSelectedStats(statsRes);
      setSelectedActivity(activityRes);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "No se pudieron cargar las estadísticas del médico.");
      setSelectedStats(null);
      setSelectedActivity(null);
    } finally {
      setIsLoadingDetails(false);
    }
  }, []);

  useEffect(() => {
    void loadDoctors();
  }, [loadDoctors]); // loadDoctors es estable gracias a useCallback

  useEffect(() => {
    if (selectedDoctorId) {
      void loadDoctorDetails(selectedDoctorId);
    } else {
      setSelectedStats(null);
      setSelectedActivity(null);
    }
  }, [selectedDoctorId, loadDoctorDetails]);

  function selectDoctor(docId: number) {
    setSelectedDoctorId(docId);
  }

  const reloadDoctorsOnly = useCallback(async () => {
    await loadDoctors(false);
  }, [loadDoctors]);

  return {
    doctors,
    selectedDoctor,
    selectedStats,
    selectedActivity,
    isLoadingDoctors,
    isLoadingDetails,
    error,
    reload: loadDoctors,
    reloadDoctorsOnly,
    selectDoctor
  };
}
