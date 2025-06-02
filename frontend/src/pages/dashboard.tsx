import type React from "react";
import {
  CurrencyDollarIcon,
  MapIcon,
  CalendarIcon,
  ArrowTrendingUpIcon,
} from "@heroicons/react/24/outline";
import { useDashboard } from "../hooks/useDashboard";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { ErrorMessage } from "../components/common/ErrorMessage";
import { EmptyState } from "../components/common/EmptyState";
import { formatCurrency, formatDateRange } from "../utils/formatters";
import { environment } from "../config/environment";
import { useNavigate } from "react-router-dom";

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { stats, activeTrips, loading, error, refetch } = useDashboard();

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

  // Provide default values to prevent undefined errors
  const safeStats = {
    totalTrips: stats?.total_trips ?? 0,
    activeTrips: stats?.active_trips ?? 0,
    totalExpenses: stats?.total_expenses ?? 0,
    avgDailyExpense: stats?.avg_daily_expense ?? 0,
  };

  const statCards = [
    {
      name: "Total Trips",
      value: safeStats.totalTrips,
      icon: MapIcon,
      color: "bg-blue-500",
    },
    {
      name: "Active Trips",
      value: safeStats.activeTrips,
      icon: CalendarIcon,
      color: "bg-green-500",
    },
    {
      name: "Total Expenses",
      value: formatCurrency(safeStats.totalExpenses),
      icon: CurrencyDollarIcon,
      color: "bg-yellow-500",
    },
    {
      name: "Avg Daily Expense",
      value: formatCurrency(safeStats.avgDailyExpense),
      icon: ArrowTrendingUpIcon,
      color: "bg-purple-500",
    },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          {environment.appName}
        </h1>
        <p className="mt-2 text-gray-600">
          Welcome back! Here's an overview of your travel expenses.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        {statCards.map((stat) => (
          <div
            key={stat.name}
            className="bg-white overflow-hidden shadow rounded-lg"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className={`${stat.color} p-3 rounded-md`}>
                    <stat.icon className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {stat.name}
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {stat.value}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Active Trips */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Active Trips
          </h3>
          {activeTrips && activeTrips.length > 0 ? (
            <div className="space-y-4">
              {activeTrips.map((trip) => (
                <div
                  key={trip.trip_id}
                  className="border rounded-lg p-4 hover:bg-gray-50 cursor-pointer"
                  onClick={() => navigate(`/trips/${trip.trip_id}`)}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-medium text-gray-900">
                        {trip.is_international
                          ? "🌍 International"
                          : "🏠 Domestic"}{" "}
                        Trip
                      </h4>
                      <p className="text-sm text-gray-500">
                        {formatDateRange(trip.start_date, trip.end_date)}
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        Daily Budget: {formatCurrency(trip.daily_budget, "COP")}
                      </p>
                    </div>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Active
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState
              icon={MapIcon}
              title="No active trips"
              description="Start tracking your travel expenses by creating a new trip."
              action={{
                label: "Create Trip",
                onClick: () => navigate("/trips/new"),
              }}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
