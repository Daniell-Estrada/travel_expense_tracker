import type React from "react";
import { ExclamationTriangleIcon } from "@heroicons/react/24/outline";
import type { ErrorState } from "../../types/common";

interface ErrorMessageProps {
  error: ErrorState;
  onRetry?: () => void;
  className?: string;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  error,
  onRetry,
  className = "",
}) => {
  return (
    <div
      className={`bg-red-50 border border-red-200 text-red-800 rounded-lg p-4 ${className}`}
    >
      <div className="flex items-center">
        <ExclamationTriangleIcon className="h-5 w-5 text-red-400 mr-2" />
        <p className="font-medium">Error</p>
      </div>
      <p className="mt-1 text-sm">{error.message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-2 text-sm font-medium text-red-600 hover:text-red-500"
        >
          Try again
        </button>
      )}
    </div>
  );
};
