interface Environment {
  apiBaseUrl: string
  appName: string
}

export const environment: Environment = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1",
  appName: import.meta.env.VITE_APP_NAME || "Travel Tracker",
}

export const validateEnvironment = (): void => {
  const requiredVars = ["VITE_API_BASE_URL"]

  for (const varName of requiredVars) {
    if (!import.meta.env[varName]) {
      throw new Error(`Missing required environment variable: ${varName}`)
    }
  }
}
