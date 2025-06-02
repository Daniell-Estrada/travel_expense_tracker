import { z } from "zod"

export const tripValidationSchema = z
  .object({
    start_date: z.string().min(1, "Start date is required"),
    end_date: z.string().min(1, "End date is required"),
    is_international: z.boolean(),
    daily_budget: z.number().positive("Budget must be positive"),
    currency: z.string().min(1, "Currency is required").max(3, "Currency code must be 3 characters"),
  })
  .refine(
    (data) => {
      const startDate = new Date(data.start_date)
      const endDate = new Date(data.end_date)
      return endDate > startDate
    },
    {
      message: "End date must be after start date",
      path: ["end_date"],
    },
  )

export const expenseValidationSchema = z.object({
  expense_date: z.string().min(1, "Date is required"),
  amount: z.number().positive("Amount must be positive"),
  payment_method: z.enum(["Cash", "Card"] as const),
  expense_type: z.enum(["Transportation", "Accommodation", "Food", "Entertainment", "Shopping", "Other"] as const),
})

export type TripFormData = z.infer<typeof tripValidationSchema>
export type ExpenseFormData = z.infer<typeof expenseValidationSchema>
