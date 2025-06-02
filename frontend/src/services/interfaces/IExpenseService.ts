import type { Expense, CreateExpenseRequest } from "../../types/expense";
import type { ApiResponse } from "../../types/common";

export interface IExpenseService {
  addExpense(expenseData: CreateExpenseRequest): Promise<ApiResponse<Expense>>;
  getTripExpenses(tripId: string): Promise<ApiResponse<Expense[]>>;
}
