"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import {
  getPatientActiveTreatment,
  getPatientClinicalHistory,
  getPatients
} from "@/lib/patients-api";
import type {
  ActiveTreatment,
  ClinicalHistory,
  PatientWithTreatment
} from "@/types/patients";

export function usePatients() {
  const [patients, setPatients] = useState<PatientWithTreatment[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<number | null>(null);
  const [selectedHistory, setSelectedHistory] = useState<ClinicalHistory[]>([]);
  const [selectedTreatment, setSelectedTreatment] = useState<ActiveTreatment | null>(null);
  const [isLoadingPatients, setIsLoadingPatients] = useState(true);
  const [isLoadingRecord, setIsLoadingRecord] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const selectedPatient = useMemo(
    () => patients.find((patient) => patient.id === selectedPatientId) ?? null,
    [patients, selectedPatientId]
  );

  const loadPatients = useCallback(async () => {
    setIsLoadingPatients(true);
    setError(null);

    try {
      const patientsResponse = await getPatients();
      const patientsWithTreatments = await Promise.all(
        patientsResponse.map(async (patient) => {
          try {
            const treatment = await getPatientActiveTreatment(patient.id);
            return {
              ...patient,
              tratamiento_activo: treatment
            };
          } catch {
            return patient;
          }
        })
      );

      setPatients(patientsWithTreatments);

      if (!selectedPatientId && patientsWithTreatments.length > 0) {
        setSelectedPatientId(patientsWithTreatments[0].id);
      }
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "No se pudieron cargar pacientes");
    } finally {
      setIsLoadingPatients(false);
    }
  }, [selectedPatientId]);

  const loadPatientRecord = useCallback(async (patientId: number) => {
    setIsLoadingRecord(true);
    setError(null);

    try {
      const [historyResponse, treatmentResponse] = await Promise.all([
        getPatientClinicalHistory(patientId),
        getPatientActiveTreatment(patientId)
      ]);

      setSelectedHistory(historyResponse);
      setSelectedTreatment(treatmentResponse);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "No se pudo cargar el expediente");
      setSelectedHistory([]);
      setSelectedTreatment(null);
    } finally {
      setIsLoadingRecord(false);
    }
  }, []);

  useEffect(() => {
    void loadPatients();
  }, [loadPatients]);

  useEffect(() => {
    if (selectedPatientId) {
      void loadPatientRecord(selectedPatientId);
    }
  }, [loadPatientRecord, selectedPatientId]);

  function selectPatient(patientId: number) {
    setSelectedPatientId(patientId);
  }

  return {
    patients,
    selectedPatient,
    selectedHistory,
    selectedTreatment,
    isLoadingPatients,
    isLoadingRecord,
    error,
    reload: loadPatients,
    selectPatient
  };
}
