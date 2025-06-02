import type { ITripService } from "./interfaces/ITripService";
import type { IApiClient } from "./interfaces/IApiClient";
import type {
  Trip,
  CreateTripRequest,
  TripStats,
  TripList,
} from "../types/trip";
import type { ApiResponse } from "../types/common";

export class TripService implements ITripService {
  private apiClient: IApiClient;

  constructor(apiClient: IApiClient) {
    this.apiClient = apiClient;
  }

  async getTrips(): Promise<ApiResponse<TripList>> {
    return this.apiClient.get<ApiResponse<TripList>>("/trips");
  }

  async getTripById(id: string): Promise<ApiResponse<Trip>> {
    return this.apiClient.get<ApiResponse<Trip>>(`/trips/${id}`);
  }

  async createTrip(tripData: CreateTripRequest): Promise<ApiResponse<Trip>> {
    return this.apiClient.post<ApiResponse<Trip>>("/trips", tripData);
  }

  async getActiveTrips(): Promise<ApiResponse<TripList>> {
    return this.apiClient.get<ApiResponse<TripList>>("/dashboard/active-trips");
  }

  async getDashboardStats(): Promise<ApiResponse<TripStats>> {
    return this.apiClient.get<ApiResponse<TripStats>>("/dashboard/stats");
  }
}
