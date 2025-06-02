export interface Trip {
  trip_id: string;
  start_date: string;
  end_date: string;
  is_international: boolean;
  daily_budget: number;
  currency: string;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface CreateTripRequest {
  start_date: string;
  end_date: string;
  is_international: boolean;
  daily_budget: number;
  currency: string;
}

export interface TripStats {
  total_trips: number;
  active_trips: number;
  total_expenses: number;
  avg_daily_expense: number;
}

export interface TripList {
  trips: Trip[];
  total: number;
}
