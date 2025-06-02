import { useEffect, useCallback } from "react";
import { useAsyncOperation } from "./useAsyncOperation";
import { serviceContainer } from "../services/ServiceContainer";
import type { TripList } from "../types/trip";

export function useTrips() {
  const fetchTripsCallback = useCallback(async () => {
    const response = await serviceContainer.tripService.getTrips();
    return response.data;
  }, []);

  const {
    data: allTrips,
    loading: tripLoading,
    error,
    execute: fetchTrips,
  } = useAsyncOperation<TripList>(fetchTripsCallback, []);

  useEffect(() => {
    let mounted = true;

    const loadTrips = async () => {
      if (mounted) {
        await fetchTrips();
      }
    };

    loadTrips();

    return () => {
      mounted = false;
    };
  }, [fetchTrips]);

  return {
    trips: allTrips?.trips || [],
    loading: tripLoading === "loading",
    error,
    refetch: fetchTrips,
  };
}
