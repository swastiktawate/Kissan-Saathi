import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import WhatIfSliders from './WhatIfSliders';
import * as client from '../api/client';

vi.mock('../api/client', () => ({
    runWhatIf: vi.fn().mockResolvedValue({
        baseline: { action: 'SELL_NOW', expected_gain: 100 },
        scenario: { action: 'ANOTHER_MANDI', expected_gain: 90 },
        delta: { action_change: true, nr_change: -10 }
    })
}));

describe('WhatIfSliders', () => {
    it('renders initial state and triggers update on slider change', async () => {
        render(<WhatIfSliders />);
        const slider = screen.getByRole('slider');
        expect(slider).toBeTruthy();

        // Change the slider value
        fireEvent.change(slider, { target: { value: 10 } });
        
        // Wait for debounce and result to show
        await waitFor(() => {
            expect(screen.getByText(/Delta: -10\.00/)).toBeTruthy();
        });
    });
});
