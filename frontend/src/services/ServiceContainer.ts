import { ApiClient } from "./ApiClient";
import { TripService } from "./TripService";
import { ExpenseService } from "./ExpenseService";
import { ReportService } from "./ReportService";
import type { ITripService } from "./interfaces/ITripService";
import type { IExpenseService } from "./interfaces/IExpenseService";
import type { IReportService } from "./interfaces/IReportService";

export class ServiceContainer {
  private static instance: ServiceContainer;
  private _tripService: ITripService;
  private _expenseService: IExpenseService;
  private _reportService: IReportService;

  private constructor() {
    const apiClient = new ApiClient();
    this._tripService = new TripService(apiClient);
    this._expenseService = new ExpenseService(apiClient);
    this._reportService = new ReportService(apiClient);
  }

  static getInstance(): ServiceContainer {
    if (!ServiceContainer.instance) {
      ServiceContainer.instance = new ServiceContainer();
    }
    return ServiceContainer.instance;
  }

  get tripService(): ITripService {
    return this._tripService;
  }

  get expenseService(): IExpenseService {
    return this._expenseService;
  }

  get reportService(): IReportService {
    return this._reportService;
  }
}

export const serviceContainer = ServiceContainer.getInstance();
