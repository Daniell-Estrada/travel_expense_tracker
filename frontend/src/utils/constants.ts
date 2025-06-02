import type { PaymentMethod, ExpenseType } from "../types/expense";

export const PAYMENT_METHODS: PaymentMethod[] = ["Cash", "Card"];

export const EXPENSE_TYPES: ExpenseType[] = [
  "Transportation",
  "Accommodation",
  "Food",
  "Entertainment",
  "Shopping",
  "Other",
];

export const CURRENCY_CODES = {
  DOMESTIC: "COP",
  DEFAULT_INTERNATIONAL: "USD",
} as const;

export const CHART_COLORS = {
  CASH: "rgba(54, 162, 235, 0.5)",
  CARD: "rgba(255, 99, 132, 0.5)",
  EXPENSE_TYPES: [
    "rgba(255, 99, 132, 0.5)",
    "rgba(54, 162, 235, 0.5)",
    "rgba(255, 206, 86, 0.5)",
    "rgba(75, 192, 192, 0.5)",
    "rgba(153, 102, 255, 0.5)",
    "rgba(255, 159, 64, 0.5)",
  ],
} as const;
