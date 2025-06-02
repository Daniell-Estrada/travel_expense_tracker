import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ChartBarIcon,
  DocumentChartBarIcon,
  ArrowTrendingUpIcon,
} from "@heroicons/react/24/outline";
import { api } from "../services/api";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from "chart.js";
import { Bar, Pie } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
);

const Reports = () => {
  const navigate = useNavigate();
  const [selectedTripId, setSelectedTripId] = useState<string | null>(null);
  const [reportType, setReportType] = useState<"daily" | "type" | "summary">(
    "daily",
  );

  const [trips, setTrips] = useState<any[]>([]);
  const [tripsLoading, setTripsLoading] = useState(true);
  const [reportData, setReportData] = useState<any>(null);
  const [reportLoading, setReportLoading] = useState(true);

  useEffect(() => {
    const fetchTrips = async () => {
      setTripsLoading(true);
      try {
        const response = await api.getTrips();
        setTrips(response.data?.trips || []);
      } catch (error) {
        console.error("Error fetching trips:", error);
      } finally {
        setTripsLoading(false);
      }
    };
    fetchTrips();
  }, []);

  useEffect(() => {
    const fetchReportData = async () => {
      if (!selectedTripId) return;

      try {
        let data;
        switch (reportType) {
          case "daily":
            data = await api.getDailyReport(selectedTripId);
            break;
          case "type":
            data = await api.getTypeReport(selectedTripId);
            break;
          case "summary":
            data = await api.getTripSummary(selectedTripId);
            break;
          default:
            throw new Error("Invalid report type");
        }

        setReportData(data.data);
      } catch (error) {
        console.error("Error fetching report data:", error);
      } finally {
        setReportLoading(false);
      }
    };

    fetchReportData();
  }, [selectedTripId, reportType]);

  const dailyChartData = {
    labels:
      reportData && reportType === "daily"
        ? Object.keys(reportData).map((date) =>
            new Date(date).toLocaleDateString(),
          )
        : [],
    datasets: [
      {
        label: "Cash",
        data:
          reportData && reportType === "daily"
            ? Object.values(reportData).map((data: any) => data.cash)
            : [],
        backgroundColor: "rgba(54, 162, 235, 0.5)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1,
      },
      {
        label: "Card",
        data:
          reportData && reportType === "daily"
            ? Object.values(reportData).map((data: any) => data.card)
            : [],
        backgroundColor: "rgba(255, 99, 132, 0.5)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1,
      },
    ],
  };

  // Prepare chart data for type report
  const typeChartData = {
    labels:
      reportData && reportType === "type"
        ? Object.keys(reportData).map((type) => type)
        : [],
    datasets: [
      {
        label: "Expenses by Type",
        data:
          reportData && reportType === "type"
            ? Object.values(reportData).map((data: any) => data.total)
            : [],
        backgroundColor: [
          "rgba(255, 99, 132, 0.5)",
          "rgba(54, 162, 235, 0.5)",
          "rgba(255, 206, 86, 0.5)",
          "rgba(75, 192, 192, 0.5)",
          "rgba(153, 102, 255, 0.5)",
          "rgba(255, 159, 64, 0.5)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  if (tripsLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Reports</h1>

      {/* Trip Selection */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Select Trip</h2>

        {trips && trips.length > 0 ? (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {trips.map((trip: any) => (
              <button
                key={trip.trip_id}
                onClick={() => setSelectedTripId(trip.trip_id)}
                className={`p-4 border rounded-lg text-left hover:bg-gray-50 ${
                  selectedTripId === trip.trip_id
                    ? "border-blue-500 ring-2 ring-blue-200"
                    : "border-gray-200"
                }`}
              >
                <h3 className="font-medium text-gray-900">
                  {trip.is_international
                    ? `(${trip.currency}) International`
                    : "Domestic"}{" "}
                  Trip
                </h3>
                <p className="text-sm text-gray-500">
                  {new Date(trip.start_date).toLocaleDateString()} -{" "}
                  {new Date(trip.end_date).toLocaleDateString()}
                </p>
                <span
                  className={`inline-flex items-center mt-2 px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    trip.is_active
                      ? "bg-green-100 text-green-800"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {trip.is_active ? "Active" : "Completed"}
                </span>
              </button>
            ))}
          </div>
        ) : (
          <div className="text-center py-6">
            <p className="text-gray-500">No trips found.</p>
            <button
              onClick={() => navigate("/trips/new")}
              className="mt-2 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
            >
              Create Trip
            </button>
          </div>
        )}
      </div>

      {selectedTripId && (
        <>
          {/* Report Type Selection */}
          <div className="bg-white shadow rounded-lg p-6 mb-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Report Type
            </h2>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <button
                onClick={() => setReportType("daily")}
                className={`p-4 border rounded-lg text-center hover:bg-gray-50 ${
                  reportType === "daily"
                    ? "border-blue-500 ring-2 ring-blue-200"
                    : "border-gray-200"
                }`}
              >
                <ChartBarIcon className="h-8 w-8 mx-auto text-blue-500" />
                <h3 className="mt-2 font-medium text-gray-900">
                  Daily Expenses
                </h3>
                <p className="text-sm text-gray-500">View expenses by day</p>
              </button>

              <button
                onClick={() => setReportType("type")}
                className={`p-4 border rounded-lg text-center hover:bg-gray-50 ${
                  reportType === "type"
                    ? "border-blue-500 ring-2 ring-blue-200"
                    : "border-gray-200"
                }`}
              >
                <DocumentChartBarIcon className="h-8 w-8 mx-auto text-blue-500" />
                <h3 className="mt-2 font-medium text-gray-900">
                  Expense Types
                </h3>
                <p className="text-sm text-gray-500">
                  View expenses by category
                </p>
              </button>

              <button
                onClick={() => setReportType("summary")}
                className={`p-4 border rounded-lg text-center hover:bg-gray-50 ${
                  reportType === "summary"
                    ? "border-blue-500 ring-2 ring-blue-200"
                    : "border-gray-200"
                }`}
              >
                <ArrowTrendingUpIcon className="h-8 w-8 mx-auto text-blue-500" />
                <h3 className="mt-2 font-medium text-gray-900">Trip Summary</h3>
                <p className="text-sm text-gray-500">
                  View overall trip statistics
                </p>
              </button>
            </div>
          </div>

          {/* Report Display */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              {reportType === "daily" && "Daily Expense Report"}
              {reportType === "type" && "Expense Type Report"}
              {reportType === "summary" && "Trip Summary"}
            </h2>

            {reportLoading ? (
              <div className="flex justify-center py-6">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
            ) : reportData ? (
              <div>
                {reportType === "daily" && (
                  <div className="h-96">
                    <Bar
                      data={dailyChartData}
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                          legend: {
                            position: "top" as const,
                          },
                          title: {
                            display: true,
                            text: "Daily Expenses (COP)",
                          },
                        },
                        scales: {
                          y: {
                            beginAtZero: true,
                          },
                        },
                      }}
                    />
                  </div>
                )}

                {reportType === "type" && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="h-80">
                      <Pie
                        data={typeChartData}
                        options={{
                          responsive: true,
                          maintainAspectRatio: false,
                          plugins: {
                            legend: {
                              position: "right" as const,
                            },
                            title: {
                              display: true,
                              text: "Expenses by Type (COP)",
                            },
                          },
                        }}
                      />
                    </div>

                    <div className="overflow-x-auto">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            <th
                              scope="col"
                              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                              Type
                            </th>
                            <th
                              scope="col"
                              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                              Cash
                            </th>
                            <th
                              scope="col"
                              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                              Card
                            </th>
                            <th
                              scope="col"
                              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                              Total
                            </th>
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {Object.entries(reportData).map(
                            ([type, data]: [string, any]) => (
                              <tr key={type}>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                  {type}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                  {data.cash?.toLocaleString()} COP
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                  {data.card?.toLocaleString()} COP
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                  {data.total?.toLocaleString()} COP
                                </td>
                              </tr>
                            ),
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {reportType === "summary" && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-gray-50 rounded-lg p-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">
                        Budget Overview
                      </h3>

                      <div className="space-y-4">
                        <div>
                          <p className="text-sm text-gray-500">Total Budget</p>
                          <p className="text-2xl font-bold text-gray-900">
                            {reportData.total_budget?.toLocaleString()} COP
                          </p>
                        </div>

                        <div>
                          <p className="text-sm text-gray-500">
                            Total Expenses
                          </p>
                          <p className="text-2xl font-bold text-gray-900">
                            {reportData.total_expenses?.toLocaleString()} COP
                          </p>
                        </div>

                        <div>
                          <p className="text-sm text-gray-500">
                            Remaining Budget
                          </p>
                          <p
                            className={`text-2xl font-bold ${reportData.remaining_budget >= 0 ? "text-green-600" : "text-red-600"}`}
                          >
                            {reportData.remaining_budget?.toLocaleString()} COP
                          </p>
                        </div>
                      </div>

                      {/* Progress bar */}
                      <div className="mt-6">
                        <div className="w-full bg-gray-200 rounded-full h-2.5">
                          <div
                            className={`h-2.5 rounded-full ${reportData.remaining_budget >= 0 ? "bg-blue-600" : "bg-red-600"}`}
                            style={{
                              width: `${Math.min(100, (reportData.total_expenses / reportData.total_budget) * 100)}%`,
                            }}
                          ></div>
                        </div>
                        <p className="mt-2 text-sm text-gray-500">
                          {Math.round(
                            (reportData.total_expenses /
                              reportData.total_budget) *
                              100,
                          )}
                          % of budget used
                        </p>
                      </div>
                    </div>

                    <div className="bg-gray-50 rounded-lg p-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">
                        Trip Statistics
                      </h3>

                      <div className="space-y-4">
                        <div>
                          <p className="text-sm text-gray-500">Trip Duration</p>
                          <p className="text-2xl font-bold text-gray-900">
                            {reportData.trip_days} days
                          </p>
                        </div>

                        <div>
                          <p className="text-sm text-gray-500">
                            Average Daily Expense
                          </p>
                          <p className="text-2xl font-bold text-gray-900">
                            {reportData.average_daily_expense?.toLocaleString()}{" "}
                            COP
                          </p>
                        </div>

                        <div>
                          <p className="text-sm text-gray-500">Budget Status</p>
                          <p
                            className={`text-lg font-medium ${reportData.remaining_budget >= 0 ? "text-green-600" : "text-red-600"}`}
                          >
                            {reportData.remaining_budget >= 0
                              ? "Within Budget"
                              : "Over Budget"}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-6">
                <p className="text-gray-500">
                  No data available for this report.
                </p>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default Reports;
