import { useState, useCallback, useRef } from "react";
import type { LoadingState, ErrorState } from "../types/common";

interface UseAsyncOperationResult<T> {
  data: T | null;
  loading: LoadingState;
  error: ErrorState | null;
  execute: (...args: any[]) => Promise<T | null>;
  reset: () => void;
}

export function useAsyncOperation<T>(
  asyncFunction: (...args: any[]) => Promise<T>,
  deps: any[] = [],
): UseAsyncOperationResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<LoadingState>("idle");
  const [error, setError] = useState<ErrorState | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const execute = useCallback(
    async (...args: any[]): Promise<T | null> => {
      // Cancel previous request if still pending
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }

      abortControllerRef.current = new AbortController();

      try {
        setLoading("loading");
        setError(null);

        const result = await asyncFunction(...args);

        // Check if request was aborted
        if (abortControllerRef.current.signal.aborted) {
          return null;
        }

        setData(result);
        setLoading("success");
        return result;
      } catch (err) {
        // Don't set error if request was aborted
        if (abortControllerRef.current?.signal.aborted) {
          return null;
        }

        const errorState: ErrorState = {
          message:
            err instanceof Error ? err.message : "An unknown error occurred",
          details: err,
        };

        setError(errorState);
        setLoading("error");
        return null;
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    deps,
  );

  const reset = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    setData(null);
    setLoading("idle");
    setError(null);
  }, []);

  return { data, loading, error, execute, reset };
}
