import { render, screen, cleanup } from '@testing-library/react';
import { describe, it, expect, afterEach } from 'vitest';
import RecommendationCard from './RecommendationCard';

describe('RecommendationCard', () => {
    afterEach(() => {
        cleanup();
    });
    it('renders action and gain for normal trust', () => {
        const data = {
            action: 'ANOTHER_MANDI',
            expected_gain_per_q: 75.5,
            meta: { trust: 'High' },
            reasons: ['Kalyan yields higher return.']
        };
        render(<RecommendationCard data={data} />);
        expect(screen.getByText(/Sell at another Mandi/)).toBeTruthy();
        expect(screen.getByText(/75\.50/)).toBeTruthy();
    });

    it('hides action badge when trust is Insufficient', () => {
        const data = {
            action: 'INSUFFICIENT_DATA',
            expected_gain_per_q: 0,
            meta: { trust: 'Insufficient' },
            reasons: ['Data too old.']
        };
        render(<RecommendationCard data={data} />);
        // Action badge should NOT appear for insufficient trust
        expect(screen.queryByText(/Sell at another Mandi/)).toBeNull();
    });

    it('shows caution banner for Medium trust', () => {
        const data = {
            action: 'SELL_NOW',
            expected_gain_per_q: 50,
            meta: { trust: 'Medium' },
            reasons: ['Selling now is marginal.']
        };
        render(<RecommendationCard data={data} />);
        expect(screen.getByText(/Caution/i)).toBeTruthy();
    });
});
