export type HealthResponse = {
  status: string;
};

export type VersionResponse = {
  version: string;
};

export async function getBackendHealth(baseUrl: string): Promise<HealthResponse> {
  const response = await fetch(`${baseUrl}/health`);
  if (!response.ok) {
    throw new Error(`Health request failed with ${response.status}`);
  }
  return response.json() as Promise<HealthResponse>;
}

export async function getBackendVersion(baseUrl: string): Promise<VersionResponse> {
  const response = await fetch(`${baseUrl}/version`);
  if (!response.ok) {
    throw new Error(`Version request failed with ${response.status}`);
  }
  return response.json() as Promise<VersionResponse>;
}
