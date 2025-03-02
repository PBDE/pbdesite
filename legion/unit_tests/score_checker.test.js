import { expect, test, describe, it } from 'vitest'
import { ScoreChecker, ScoreChecker } from '../javascript/score_checker.js';

// test game manager roll

describe('CheckCombinations', () => {

    const scoreChecker = new ScoreChecker();

    test('six of a kind should be true', () => {

        const diceArray = ['m', 'm', 'm', 'm', 'm', 'm'];
        const combinations = scoreChecker.CheckCombinations(diceArray);
        expect(combinations.sixOfAKind).toBe(true);
        expect(combinations.threePairs).toBe(true);
        expect(combinations.oneOfEach).toBe(false);
    });

    test('one of each should be true', () => {

        const diceArray = ['v', 'x', 'l', 'c', 'd', 'm'];
        const combinations = scoreChecker.CheckCombinations(diceArray);
        expect(combinations.oneOfEach).toBe(true);
        expect(combinations.sixOfAKind).toBe(false);
        expect(combinations.threePairs).toBe(false);
    });

    test('three pairs should be true', () => {

        const diceArray = ['l', 'l', 'x', 'x', 'm', 'm'];
        const combinations = scoreChecker.CheckCombinations(diceArray);
        expect(combinations.threePairs).toBe(true);
        expect(combinations.oneOfEach).toBe(false);
        expect(combinations.sixOfAKind).toBe(false);
    });

    test('three Ms should be true', () => {
        
        const diceArray = ['l', 'c', 'x', 'm', 'm', 'm'];
        const combinations = scoreChecker.CheckCombinations(diceArray);
        expect(combinations.threeMs).toBe(true);
    });

    test('three Ds should be true', () => {
        
        const diceArray = ['l', 'c', 'x', 'd', 'd', 'd'];
        const combinations = scoreChecker.CheckCombinations(diceArray);
        expect(combinations.threeDs).toBe(true);
    });

    test('three Cs should be true', () => {
        
        const diceArray = ['l', 'c', 'x', 'c', 'c', 'd'];
        const combinations = scoreChecker.CheckCombinations(diceArray);
        expect(combinations.threeCs).toBe(true);
    });

    test('three Ls should be true', () => {
        
        const diceArray = ['l', 'c', 'x', 'l', 'l', 'd'];
        const combinations = scoreChecker.CheckCombinations(diceArray);
        expect(combinations.threeLs).toBe(true);
    });

    test('four Vs should be true', () => {
        
        const diceArray = ['l', 'c', 'v', 'v', 'v', 'v'];
        const combinations = scoreChecker.CheckCombinations(diceArray);
        expect(combinations.fourVs).toBe(true);
    });
});

// describe('CalculateScoreIncompleteArray', () => {

// });

// describe('CreateScoringArray', () => {

// });

