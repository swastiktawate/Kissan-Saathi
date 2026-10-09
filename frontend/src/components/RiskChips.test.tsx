import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import RiskChips from './RiskChips';

describe('RiskChips', () => {
    it('renders "no reliable signal" when empty', () => {
        render(<RiskChips risks={[]} />);
        expect(screen.getByText(/No reliable risk signals/)).toBeTruthy();
    });

    it('renders risk flag names', () => {
        const risks = [
            { name: 'Price Drop', value: '40%', threshold: '> 30%', explanation: 'Glut expected.' }
        ];
        render(<RiskChips risks={risks} />);
        expect(screen.getByText(/Price Drop/)).toBeTruthy();
    });
});
