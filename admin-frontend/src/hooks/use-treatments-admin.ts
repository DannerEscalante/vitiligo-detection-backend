"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import {
  getTreatmentTypeStats,
  getTreatmentTypesAdmin
} from "@/lib/treatments-api";
import type { TreatmentTypeAdmin, TreatmentTypeStats } from "@/types/treatments";

export function useTreatmentsAdmin() {
  const [treatments, setTreatments] = useState<TreatmentTypeAdmin[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [selectedStats, setSelectedStats] = useState<TreatmentTypeStats | null>(null);

  const [isLoadingList, setIsLoadingList] = useState(true);
  const [isLoadingStats, setIsLoadingStats] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const selectedTreatment = useMemo(
    () => treatments.find((t) => t.id === selectedId) ?? null,
    [treatments, selectedId]
  );

  const loadTreatments = useCallback(async (selectFirst = true) => {
    setIsLoadingList(true);
    setError(null);

    try {
      const data = await getTreatmentTypesAdmin();
      setTreatments(data);

      if (selectFirst && data.length > 0 && !selectedId) {
        setSelectedId(data[0].id);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo cargar el catálogo de tratamientos.");
    } finally {
      setIsLoadingList(false);
    }
  }, [selectedId]);

  const loadStats = useCallback(async (id: number) => {
    setIsLoadingStats(true);
    setError(null);

    try {
      const stats = await getTreatmentTypeStats(id);
      setSelectedStats(stats);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudieron cargar las estadísticas.");
      setSelectedStats(null);
    } finally {
      setIsLoadingStats(false);
    }
  }, []);

  // Carga inicial
  useEffect(() => {
    void loadTreatments();
  }, [loadTreatments]);

  // Carga de estadísticas al cambiar selección
  useEffect(() => {
    if (selectedId) {
      void loadStats(selectedId);
    } else {
      setSelectedStats(null);
    }
  }, [selectedId, loadStats]);

  function selectTreatment(id: number) {
    setSelectedId(id);
  }

  const reloadList = useCallback(async () => {
    await loadTreatments(false);
  }, [loadTreatments]);

  // Refresca stats del item seleccionado (post-edición)
  const reloadSelectedStats = useCallback(async () => {
    if (selectedId) {
      await loadStats(selectedId);
    }
  }, [selectedId, loadStats]);

  return {
    treatments,
    selectedTreatment,
    selectedStats,
    isLoadingList,
    isLoadingStats,
    error,
    selectTreatment,
    reload: loadTreatments,
    reloadList,
    reloadSelectedStats
  };
}
