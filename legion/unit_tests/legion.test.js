import { expect, test, describe, it } from 'vitest'
import { ScoreChecker } from '../static/legion/javascript/legion.js'

// test game manager roll

describe('CheckCombinations', () => {

    test('six of a kind should be true', () => {

        const diceArray = ['m', 'm', 'm', 'm', 'm', 'm'];

        const combinations = ScoreChecker.CheckCombinations(diceArray);

        expect(combinations.sixOfAKind).toBe(true);

    });

});

describe('CalculateScoreIncompleteArray', () => {

});

describe('CreateScoringArray', () => {

});

