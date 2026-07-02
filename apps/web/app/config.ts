export const appConfig = {
  appVersion: process.env.NEXT_PUBLIC_APP_VERSION ?? '0.1.0a0',
  environment: process.env.NEXT_PUBLIC_ENVIRONMENT ?? 'development',
  architectureVersion: process.env.NEXT_PUBLIC_ARCHITECTURE_VERSION ?? 'GAR-0001',
  sprintVersion: process.env.NEXT_PUBLIC_SPRINT_VERSION ?? 'GAR-SPRINT-0001',
  backendBaseUrl: process.env.NEXT_PUBLIC_BACKEND_URL ?? 'http://localhost:8000',
};
