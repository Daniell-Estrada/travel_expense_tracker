import type { IReportService } from "./interfaces/IReportService";
import type { IApiClient } from "./interfaces/IApiClient";
import type { DailyReport, TypeReport, TripSummary } from "../types/report";
import type { ApiResponse } from "../types/common";

export class ReportService implements IReportService {
  private apiClient: IApiClient;

  constructor(apiClient: IApiClient) {
    this.apiClient = apiClient;
  }

  async getDailyReport(tripId: string): Promise<ApiResponse<DailyReport>> {
    return this.apiClient.get<ApiResponse<DailyReport>>(
      `/reports/daily/${tripId}`,
    );
  }

  async getTypeReport(tripId: string): Promise<ApiResponse<TypeReport>> {
    return this.apiClient.get<ApiResponse<TypeReport>>(
      `/reports/type/${tripId}`,
    );
  }

  async getTripSummary(tripId: string): Promise<ApiResponse<TripSummary>> {
    return this.apiClient.get<ApiResponse<TripSummary>>(
      `/reports/summary/${tripId}`,
    );
  }
}
