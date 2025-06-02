import { useEffect, useCallback } from "react";
import { useAsyncOperation } from "./useAsyncOperation";
import { serviceContainer } from "../services/ServiceContainer";
import type { TripList, TripStats } from "../types/trip";

export function useDashboard() {
  const fetchStatsCallback = useCallback(async () => {
    const response = await serviceContainer.tripService.getDashboardStats();
    return response.data;
  }, []);

  const fetchActiveTripsCallback = useCallback(async () => {
    const response = await serviceContainer.tripService.getActiveTrips();
    return response.data;
  }, []);

  const {
    data: stats,
    loading: statsLoading,
    error: statsError,
    execute: fetchStats,
  } = useAsyncOperation<TripStats>(fetchStatsCallback, []);

  const {
    data: activeTrips,
    loading: tripsLoading,
    error: tripsError,
    execute: fetchActiveTrips,
  } = useAsyncOperation<TripList>(fetchActiveTripsCallback, []);

  useEffect(() => {
    let mounted = true;

    const loadData = async () => {
      if (mounted) {
        await Promise.all([fetchStats(), fetchActiveTrips()]);
      }
    };

    loadData();

    return () => {
      mounted = false;
    };
  }, [fetchStats, fetchActiveTrips]);

  const refetch = useCallback(() => {
    fetchStats();
    fetchActiveTrips();
  }, [fetchStats, fetchActiveTrips]);

  return {
    stats,
    activeTrips: activeTrips?.trips || [],
    loading: statsLoading === "loading" || tripsLoading === "loading",
    error: statsError || tripsError,
    refetch,
  };
}
