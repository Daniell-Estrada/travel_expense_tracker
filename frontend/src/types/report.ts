export interface DailyReport {
  [date: string]: {
    cash: number
    card: number
    total: number
  }
}

export interface TypeReport {
  [type: string]: {
    cash: number
    card: number
    total: number
  }
}

export interface TripSummary {
  total_budget: number
  total_expenses: number
  remaining_budget: number
  trip_days: number
  average_daily_expense: number
}
