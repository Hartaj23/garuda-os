import { getBackendHealth, getBackendVersion } from '@/lib/api';

describe('api client', () => {
  beforeEach(() => {
    global.fetch = jest.fn() as jest.Mock;
  });

  it('requests the health endpoint and parses the response', async () => {
    (global.fetch as jest.Mock).mockResolvedValue({ ok: true, json: async () => ({ status: 'ok' }) });

    const response = await getBackendHealth('http://localhost:8000');

    expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/health');
    expect(response).toEqual({ status: 'ok' });
  });

  it('requests the version endpoint and parses the response', async () => {
    (global.fetch as jest.Mock).mockResolvedValue({ ok: true, json: async () => ({ version: '0.1.0a0' }) });

    const response = await getBackendVersion('http://localhost:8000');

    expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/version');
    expect(response).toEqual({ version: '0.1.0a0' });
  });
});
