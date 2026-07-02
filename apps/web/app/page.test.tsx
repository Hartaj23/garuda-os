import { render, screen, waitFor } from '@testing-library/react';
import HomePage from './page';

jest.mock('@/lib/api', () => ({
  getBackendHealth: jest.fn().mockResolvedValue({ status: 'ok' }),
  getBackendVersion: jest.fn().mockResolvedValue({ version: '0.1.0a0' }),
}));

describe('HomePage', () => {
  it('renders the dashboard shell and backend status', async () => {
    render(<HomePage />);

    expect(screen.getByText('Garuda OS')).toBeInTheDocument();
    expect(screen.getByText(/Application/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Connected backend: http://localhost:8000')).toBeInTheDocument();
    });
  });
});
