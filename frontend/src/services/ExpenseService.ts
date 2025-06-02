import type { IExpenseService } from "./interfaces/IExpenseService";
import type { IApiClient } from "./interfaces/IApiClient";
import type { Expense, CreateExpenseRequest } from "../types/expense";
import type { ApiResponse } from "../types/common";

export class ExpenseService implements IExpenseService {
  private apiClient: IApiClient;

  constructor(apiClient: IApiClient) {
    this.apiClient = apiClient;
  }

  async addExpense(
    expenseData: CreateExpenseRequest,
  ): Promise<ApiResponse<Expense>> {
    const expenseWithId = {
      ...expenseData,
      expense_id: crypto.randomUUID(),
      expense_date: new Date(expenseData.expense_date).toISOString(),
    };

    return this.apiClient.post<ApiResponse<Expense>>(
      "/expenses",
      expenseWithId,
    );
  }

  async getTripExpenses(tripId: string): Promise<ApiResponse<Expense[]>> {
    return this.apiClient.get<ApiResponse<Expense[]>>(`/expenses/${tripId}`);
  }
}
