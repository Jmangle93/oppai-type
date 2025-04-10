import { describe, it, expect } from 'vitest';
import { CharacterTracker } from '../src/tracker.js';

describe('CharacterTracker', () => {
    it('initializes stats correctly', () => {
        const tracker = new CharacterTracker([['ka', 'カ']]);
        expect(tracker.stats['ka|カ']).toBeInstanceOf(CharacterStats);
    });
    it('updates stats correctly', () => {
        const tracker = new CharacterTracker([['ka', 'カ']]);
        tracker.updateStats('ka', 'カ', 1.5, true);
        expect(tracker.stats['ka|カ'].attempts).toBe(1);
    });
});