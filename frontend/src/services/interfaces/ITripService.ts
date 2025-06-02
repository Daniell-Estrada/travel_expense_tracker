import type {
  Trip,
  CreateTripRequest,
  TripStats,
  TripList,
} from "../../types/trip";
import type { ApiResponse } from "../../types/common";

export interface ITripService {
  getTrips(): Promise<ApiResponse<TripList>>;
  getTripById(id: string): Promise<ApiResponse<Trip>>;
  createTrip(tripData: CreateTripRequest): Promise<ApiResponse<Trip>>;
  getActiveTrips(): Promise<ApiResponse<TripList>>;
  getDashboardStats(): Promise<ApiResponse<TripStats>>;
}
