import type React from "react";
import { useState } from "react";
import { Link } from "react-router-dom";
import {
  PlusIcon,
  MapPinIcon,
  CalendarIcon,
  CurrencyDollarIcon,
} from "@heroicons/react/24/outline";
import { useTrips } from "../hooks/useTrips";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { ErrorMessage } from "../components/common/ErrorMessage";
import { EmptyState } from "../components/common/EmptyState";
import { formatDateRange, formatCurrency } from "../utils/formatters";
import type { Trip } from "../types/trip";

type FilterType = "all" | "active" | "completed";

const Trips: React.FC = () => {
  const [filter, setFilter] = useState<FilterType>("all");
  const { trips, loading, error, refetch } = useTrips();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage error={error} onRetry={refetch} />;
  }

  const filteredTrips = trips.filter((trip: Trip) => {
    if (filter === "active") return trip.is_active;
    if (filter === "completed") return !trip.is_active;
    return true;
  });

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">My Trips</h1>
        <Link
          to="/trips/new"
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
        >
          <PlusIcon className="-ml-1 mr-2 h-5 w-5" />
          New Trip
        </Link>
      </div>

      {/* Filter tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          {(["all", "active", "completed"] as FilterType[]).map((tab) => (
            <button
              key={tab}
              onClick={() => setFilter(tab)}
              className={`${
                filter === tab
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm capitalize`}
            >
              {tab}
            </button>
          ))}
        </nav>
      </div>

      {filteredTrips.length === 0 ? (
        <EmptyState
          icon={MapPinIcon}
          title="No trips found"
          description="Get started by creating a new trip."
          action={{
            label: "New Trip",
            onClick: () => {},
          }}
        />
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {filteredTrips.map((trip: Trip) => (
            <Link
              key={trip.trip_id}
              to={`/trips/${trip.trip_id}`}
              className="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow duration-300"
            >
              <div className="p-5">
                <div className="flex items-center">
                  <div
                    className={`p-2 rounded-md ${trip.is_international ? "bg-purple-100" : "bg-blue-100"}`}
                  >
                    <MapPinIcon
                      className={`h-6 w-6 ${trip.is_international ? "text-purple-600" : "text-blue-600"}`}
                    />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-medium text-gray-900">
                      {trip.is_international
                        ? `(${trip.currency}) International`
                        : "Domestic"}{" "}
                      Trip
                    </h3>
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        trip.is_active
                          ? "bg-green-100 text-green-800"
                          : "bg-gray-100 text-gray-800"
                      }`}
                    >
                      {trip.is_active ? "Active" : "Completed"}
                    </span>
                  </div>
                </div>
                <div className="mt-4 space-y-2">
                  <div className="flex items-center text-sm text-gray-500">
                    <CalendarIcon className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
                    <span>
                      {formatDateRange(trip.start_date, trip.end_date)}
                    </span>
                  </div>
                  <div className="flex items-center text-sm text-gray-500">
                    <CurrencyDollarIcon className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
                    <span>
                      {formatCurrency(trip.daily_budget, "COP")} / day
                    </span>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default Trips;
