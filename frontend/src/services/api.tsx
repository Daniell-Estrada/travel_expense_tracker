const API_BASE_URL = "http://localhost:8000/api/v1";
import axios from "axios";

class ApiService {
  // Dashboard
  async getDashboardStats() {
    return await axios.get(`${API_BASE_URL}/dashboard/stats`);
  }

  async getActiveTrips() {
    return await axios.get(`${API_BASE_URL}/dashboard/active-trips`);
  }

  // Trips
  async getTrips() {
    return await axios.get(`${API_BASE_URL}/trips`);
  }

  async getTripById(id: string) {
    return await axios.get(`${API_BASE_URL}/trips/${id}`);
  }

  async createTrip(tripData: any) {
    return await axios.post(`${API_BASE_URL}/trips`, tripData);
  }

  // Expenses
  async addExpense(expenseData: any) {
    return await axios.post(`${API_BASE_URL}/expenses`, expenseData);
  }

  async getTripExpenses(tripId: string) {
    return await axios.get(`${API_BASE_URL}/expenses/${tripId}`);
  }

  // Reports
  async getDailyReport(tripId: string) {
    return await axios.get(`${API_BASE_URL}/reports/daily/${tripId}`);
  }

  async getTypeReport(tripId: string) {
    return await axios.get(`${API_BASE_URL}/reports/type/${tripId}`);
  }

  async getTripSummary(tripId: string) {
    return await axios.get(`${API_BASE_URL}/reports/summary/${tripId}`);
  }
}

export const api = new ApiService();
