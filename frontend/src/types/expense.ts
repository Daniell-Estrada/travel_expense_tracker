export type PaymentMethod = "Cash" | "Card"
export type ExpenseType = "Transportation" | "Accommodation" | "Food" | "Entertainment" | "Shopping" | "Other"

export interface Expense {
  expense_id: string
  trip_id: string
  expense_date: string
  amount: number
  payment_method: PaymentMethod
  expense_type: ExpenseType
  currency: string
  converted_amount: number
  created_at?: string
  updated_at?: string
}

export interface CreateExpenseRequest {
  trip_id: string
  expense_date: string
  amount: number
  payment_method: PaymentMethod
  expense_type: ExpenseType
}
