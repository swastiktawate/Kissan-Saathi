import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import OfflineBanner from './OfflineBanner';
import * as useOfflineHook from '../hooks/useOffline';

vi.mock('../hooks/useOffline', () => ({
    useOffline: vi.fn()
}));

describe('OfflineBanner', () => {
    it('renders banner when offline', () => {
        vi.mocked(useOfflineHook.useOffline).mockReturnValue({
            isOffline: true,
            lastSync: '2023-10-09'
        });
        render(<OfflineBanner />);
        expect(screen.getByText(/Offline — showing last result from 2023-10-09/)).toBeTruthy();
    });

    it('does not render when online', () => {
        vi.mocked(useOfflineHook.useOffline).mockReturnValue({
            isOffline: false,
            lastSync: null
        });
        const { container } = render(<OfflineBanner />);
        expect(container.firstChild).toBeNull();
    });
});
