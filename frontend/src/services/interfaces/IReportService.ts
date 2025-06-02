import type { DailyReport, TypeReport, TripSummary } from "../../types/report";
import type { ApiResponse } from "../../types/common";

export interface IReportService {
  getDailyReport(tripId: string): Promise<ApiResponse<DailyReport>>;
  getTypeReport(tripId: string): Promise<ApiResponse<TypeReport>>;
  getTripSummary(tripId: string): Promise<ApiResponse<TripSummary>>;
}
