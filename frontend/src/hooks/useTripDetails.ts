import { useEffect, useCallback } from "react";
import { useAsyncOperation } from "./useAsyncOperation";
import { serviceContainer } from "../services/ServiceContainer";
import type { Trip } from "../types/trip";
import type { Expense } from "../types/expense";

export function useTripDetails(tripId: string | undefined) {
  const fetchTripCallback = useCallback(async (id: string) => {
    const response = await serviceContainer.tripService.getTripById(id);
    return response.data;
  }, []);

  const fetchExpensesCallback = useCallback(async (id: string) => {
    const response = await serviceContainer.expenseService.getTripExpenses(id);
    return response.data;
  }, []);

  const {
    data: trip,
    loading: tripLoading,
    error: tripError,
    execute: fetchTrip,
  } = useAsyncOperation<Trip>(fetchTripCallback, [tripId]);

  const {
    data: expenses,
    loading: expensesLoading,
    error: expensesError,
    execute: fetchExpenses,
  } = useAsyncOperation<Expense[]>(fetchExpensesCallback, [tripId]);

  useEffect(() => {
    let mounted = true;

    const loadTripData = async () => {
      if (tripId && mounted) {
        await Promise.all([fetchTrip(tripId), fetchExpenses(tripId)]);
      }
    };

    loadTripData();

    return () => {
      mounted = false;
    };
  }, [tripId, fetchTrip, fetchExpenses]);

  const refetchTrip = useCallback(() => {
    if (tripId) fetchTrip(tripId);
  }, [tripId, fetchTrip]);

  const refetchExpenses = useCallback(() => {
    if (tripId) fetchExpenses(tripId);
  }, [tripId, fetchExpenses]);

  return {
    trip,
    expenses: expenses || [],
    loading: tripLoading === "loading" || expensesLoading === "loading",
    error: tripError || expensesError,
    refetchTrip,
    refetchExpenses,
  };
}
