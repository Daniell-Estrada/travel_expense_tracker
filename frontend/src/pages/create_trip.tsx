import type React from "react";

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import toast from "react-hot-toast";
import { api } from "../services/api";

// Form validation schema
const tripSchema = z.object({
  start_date: z.string().min(1, "Start date is required"),
  end_date: z.string().min(1, "End date is required"),
  is_international: z.boolean(),
  daily_budget: z.number().positive("Budget must be positive"),
  currency: z
    .string()
    .min(1, "Currency is required")
    .max(3, "Currency code must be 3 characters"),
});

type TripFormData = z.infer<typeof tripSchema>;

const CreateTrip = () => {
  const navigate = useNavigate();
  const [isInternational, setIsInternational] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch,
  } = useForm<TripFormData>({
    resolver: zodResolver(tripSchema),
    defaultValues: {
      is_international: false,
      currency: "COP",
      daily_budget: 0,
    },
  });

  const createTripMutation = useMutation({
    mutationFn: api.createTrip,
    onSuccess: () => {
      toast.success("Trip created successfully!");
      navigate("/trips");
    },
    onError: (error) => {
      toast.error(
        `Failed to create trip: ${error instanceof Error ? error.message : "Unknown error"}`,
      );
    },
  });

  const onSubmit = (data: TripFormData) => {
    // Ensure dates are in the correct format
    createTripMutation.mutate({
      ...data,
      daily_budget: Number(data.daily_budget),
    });
  };

  // Watch for international status changes
  const watchIsInternational = watch("is_international");

  // Update currency when international status changes
  const handleInternationalChange = (
    e: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const isChecked = e.target.checked;
    setIsInternational(isChecked);
    setValue("is_international", isChecked);

    // Reset currency to COP for domestic trips
    if (!isChecked) {
      setValue("currency", "COP");
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Create New Trip</h1>

      <div className="bg-white shadow rounded-lg p-6">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Date Range */}
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label
                htmlFor="start_date"
                className="block text-sm font-medium text-gray-700"
              >
                Start Date
              </label>
              <input
                type="date"
                id="start_date"
                {...register("start_date")}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
              {errors.start_date && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.start_date.message}
                </p>
              )}
            </div>

            <div>
              <label
                htmlFor="end_date"
                className="block text-sm font-medium text-gray-700"
              >
                End Date
              </label>
              <input
                type="date"
                id="end_date"
                {...register("end_date")}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
              {errors.end_date && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.end_date.message}
                </p>
              )}
            </div>
          </div>

          {/* International Toggle */}
          <div className="flex items-center">
            <input
              id="is_international"
              type="checkbox"
              {...register("is_international")}
              onChange={handleInternationalChange}
              className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <label
              htmlFor="is_international"
              className="ml-2 block text-sm text-gray-900"
            >
              International Trip
            </label>
          </div>

          {/* Currency and Budget */}
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label
                htmlFor="currency"
                className="block text-sm font-medium text-gray-700"
              >
                Currency
              </label>
              <input
                type="text"
                id="currency"
                {...register("currency")}
                disabled={!watchIsInternational}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 disabled:bg-gray-100"
              />
              {errors.currency && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.currency.message}
                </p>
              )}
            </div>

            <div>
              <label
                htmlFor="daily_budget"
                className="block text-sm font-medium text-gray-700"
              >
                Daily Budget
              </label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-gray-500 sm:text-sm">$</span>
                </div>
                <input
                  type="number"
                  id="daily_budget"
                  {...register("daily_budget", { valueAsNumber: true })}
                  className="block w-full pl-7 pr-12 rounded-md border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                  placeholder="0.00"
                />
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <span className="text-gray-500 sm:text-sm">COP</span>
                </div>
              </div>
              {errors.daily_budget && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.daily_budget.message}
                </p>
              )}
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex justify-end">
            <button
              type="button"
              onClick={() => navigate("/trips")}
              className="mr-3 px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={createTripMutation.isLoading}
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-300"
            >
              {createTripMutation.isLoading ? "Creating..." : "Create Trip"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateTrip;
