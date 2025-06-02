import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import {
  CalendarIcon,
  MapPinIcon,
  CurrencyDollarIcon,
  PlusIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
} from "@heroicons/react/24/outline";
import { api } from "../services/api";

// Form validation schema for expenses
const expenseSchema = z.object({
  expense_date: z.string().min(1, "Date is required"),
  amount: z.number().positive("Amount must be positive"),
  payment_method: z.enum(["Cash", "Card"]),
  expense_type: z.enum([
    "Transportation",
    "Accommodation",
    "Food",
    "Entertainment",
    "Shopping",
    "Other",
  ]),
});

type ExpenseFormData = z.infer<typeof expenseSchema>;

const TripDetails = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [trip, setTrip] = useState<any>(null);
  const [expenses, setExpenses] = useState<any[]>([]);
  const [showExpenseForm, setShowExpenseForm] = useState(false);
  const [tripLoading, setTripLoading] = useState(true);
  const [expensesLoading, setExpensesLoading] = useState(true);

  useEffect(() => {
    if (!id) return;

    // Fetch trip details
    const fetchTrip = async () => {
      try {
        const response = await api.getTripById(id);
        setTrip(response.data);
      } catch (error) {
        console.error("Error fetching trip:", error);
        toast.error("Failed to load trip details.");
      } finally {
        setTripLoading(false);
      }
    };

    // Fetch expenses for the trip
    const fetchExpenses = async () => {
      try {
        const response = await api.getTripExpenses(id);
        setExpenses(response.data);
      } catch (error) {
        console.error("Error fetching expenses:", error);
        toast.error("Failed to load expenses.");
      } finally {
        setExpensesLoading(false);
      }
    };

    fetchTrip();
    fetchExpenses();
  }, [id]);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ExpenseFormData>({
    resolver: zodResolver(expenseSchema),
    defaultValues: {
      payment_method: "Cash",
      expense_type: "Other",
    },
  });

  const onSubmit = (data: ExpenseFormData) => {
    if (!id) return;

    const expenseData = {
      ...data,
      expense_id: crypto.randomUUID(),
      trip_id: id,
      expense_date: new Date(data.expense_date).toISOString(),
    };

    api
      .addExpense(expenseData)
      .then(() => {
        api.getTripExpenses(id).then((res) => setExpenses(res.data));
        toast.success("Expense added successfully!");
        setShowExpenseForm(false);
      })
      .catch((error) => {
        console.error("Error adding expense:", error);
        toast.error("Failed to add expense.");
      });
  };

  if (tripLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!trip) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-800 rounded-lg p-4">
        <p>Trip not found.</p>
        <button
          onClick={() => navigate("/trips")}
          className="mt-2 text-sm font-medium text-red-600 hover:text-red-500"
        >
          Back to Trips
        </button>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">
          {trip.is_international ? "International" : "Domestic"} Trip
        </h1>
        <div className="flex space-x-2">
          <button
            onClick={() => navigate("/reports")}
            className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            View Reports
          </button>
          {trip.is_active && (
            <button
              onClick={() => setShowExpenseForm(!showExpenseForm)}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
            >
              <PlusIcon className="-ml-1 mr-2 h-5 w-5" />
              Add Expense
            </button>
          )}
        </div>
      </div>

      {/* Trip Info Card */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flex items-center">
            <CalendarIcon className="h-8 w-8 text-blue-500" />
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-500">Date Range</h3>
              <p className="text-lg text-gray-900">
                {new Date(trip.start_date).toLocaleDateString()} -{" "}
                {new Date(trip.end_date).toLocaleDateString()}
              </p>
            </div>
          </div>

          <div className="flex items-center">
            <MapPinIcon className="h-8 w-8 text-blue-500" />
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-500">Trip Type</h3>
              <p className="text-lg text-gray-900">
                {trip.is_international ? "International" : "Domestic"}
              </p>
            </div>
          </div>

          <div className="flex items-center">
            <CurrencyDollarIcon className="h-8 w-8 text-blue-500" />
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-500">
                Daily Budget
              </h3>
              <p className="text-lg text-gray-900">
                {trip.daily_budget.toLocaleString()} COP
              </p>
            </div>
          </div>
        </div>

        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="flex items-center">
            <div
              className={`p-1 rounded-full ${trip.is_active ? "bg-green-100" : "bg-gray-100"}`}
            >
              {trip.is_active ? (
                <CheckCircleIcon className="h-5 w-5 text-green-500" />
              ) : (
                <ExclamationCircleIcon className="h-5 w-5 text-gray-500" />
              )}
            </div>
            <span className="ml-2 text-sm font-medium text-gray-700">
              Status: {trip.is_active ? "Active" : "Completed"}
            </span>
          </div>
        </div>
      </div>

      {/* Add Expense Form */}
      {showExpenseForm && (
        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">
            Add New Expense
          </h2>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <label
                  htmlFor="expense_date"
                  className="block text-sm font-medium text-gray-700"
                >
                  Date
                </label>
                <input
                  type="date"
                  id="expense_date"
                  {...register("expense_date")}
                  min={trip.start_date}
                  max={trip.end_date}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
                {errors.expense_date && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.expense_date.message}
                  </p>
                )}
              </div>

              <div>
                <label
                  htmlFor="amount"
                  className="block text-sm font-medium text-gray-700"
                >
                  Amount
                </label>
                <div className="mt-1 relative rounded-md shadow-sm">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <span className="text-gray-500 sm:text-sm">$</span>
                  </div>
                  <input
                    type="number"
                    id="amount"
                    step="0.01"
                    {...register("amount", { valueAsNumber: true })}
                    className="block w-full pl-7 pr-12 rounded-md border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                    placeholder="0.00"
                  />
                  <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                    <span className="text-gray-500 sm:text-sm">
                      {trip.currency}
                    </span>
                  </div>
                </div>
                {errors.amount && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.amount.message}
                  </p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <label
                  htmlFor="payment_method"
                  className="block text-sm font-medium text-gray-700"
                >
                  Payment Method
                </label>
                <select
                  id="payment_method"
                  {...register("payment_method")}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value="Cash">Cash</option>
                  <option value="Card">Card</option>
                </select>
              </div>

              <div>
                <label
                  htmlFor="expense_type"
                  className="block text-sm font-medium text-gray-700"
                >
                  Expense Type
                </label>
                <select
                  id="expense_type"
                  {...register("expense_type")}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value="Transportation">Transportation</option>
                  <option value="Accommodation">Accommodation</option>
                  <option value="Food">Food</option>
                  <option value="Entertainment">Entertainment</option>
                  <option value="Shopping">Shopping</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>

            <div className="flex justify-end">
              <button
                type="button"
                onClick={() => setShowExpenseForm(false)}
                className="mr-3 px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-300"
              >
                Add Expense
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Expenses List */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-4 py-5 sm:px-6">
          <h2 className="text-lg font-medium text-gray-900">Expenses</h2>
          <p className="mt-1 text-sm text-gray-500">
            List of all expenses for this trip
          </p>
        </div>

        {expensesLoading ? (
          <div className="flex justify-center py-6">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : expenses && expenses.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Date
                  </th>
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
                    Payment
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Amount
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Converted (COP)
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {expenses.map((expense: any) => (
                  <tr key={expense.expense_id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {new Date(expense.expense_date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {expense.expense_type}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {expense.payment_method}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {expense.amount} {expense.currency}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {expense.converted_amount}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-6">
            <p className="text-gray-500">No expenses found for this trip.</p>
            {trip.is_active && (
              <button
                onClick={() => setShowExpenseForm(true)}
                className="mt-2 inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded text-blue-700 bg-blue-100 hover:bg-blue-200"
              >
                <PlusIcon className="-ml-0.5 mr-1 h-4 w-4" />
                Add Expense
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default TripDetails;
