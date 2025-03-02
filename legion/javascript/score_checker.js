import { dieFaces } from "./support.js";

class ScoreChecker {

    #combinations;

    CheckScore(currentRoll){

        this.#combinations = this.CheckCombinations(currentRoll);
        const scoring = this.#CreateScoringArray(this.#combinations, currentRoll);
        const rollScore = this.#CalculateScoreFromCombinations(currentRoll);
        const rollMessage = this.#CreateScoreMessage(this.#combinations, currentRoll);

        return { scoring: scoring, combinations: this.#combinations, rollScore: rollScore, rollMessage: rollMessage }
    }

    CheckCombinations(diceArray){

        const counts = this.#CountValues(diceArray);

        const ThreePairs = function(counts){
            let pairsCount = 0
            Object.values(counts).forEach(function(count){
                pairsCount += Math.trunc(count/2);
            });
            return pairsCount === 3;
        }

        const combinations = {
            'sixOfAKind': diceArray.length === 6 && diceArray.every(value => value === diceArray[0]),
            'oneOfEach': diceArray.length === 6 && Object.values(counts).every(value => value === 1),
            'threePairs': ThreePairs(counts),
            'threeMs': this.ThreeMs(diceArray),
            'threeDs': this.ThreeDs(diceArray),
            'threeCs': this.ThreeCs(diceArray),
            'threeLs': this.ThreeLs(diceArray),
            'fourVs': diceArray.filter(value => value === dieFaces.v).length >= 4,
            'xsOrVs': diceArray.includes(dieFaces.v) || diceArray.includes(dieFaces.x)
        }
        return combinations;
    }

    CalculateScoreIncompleteArray(diceArray){ // too much repitition - create a three of a kind method

        let score = 0;

        if (this.ThreeMs(diceArray)){ score = 1000; }
        if (this.ThreeDs(diceArray)){ score += 500; }
        if (this.ThreeCs(diceArray)){ score += 100; }
        if (this.ThreeLs(diceArray)){ score += 50; }
        score += diceArray.filter(value => value === dieFaces.x).length * 10;
        score += diceArray.filter(value => value === dieFaces.v).length * 5;
        return score;
    }

    #CreateScoringArray(combinations, currentRoll){

        const counts = this.#CountValues(currentRoll);

        let scoring = []

        if(combinations.fourVs) { return scoring; }

        if(combinations.oneOfEach || combinations.sixOfAKind || combinations.threePairs){
            return currentRoll;
        }
        if (combinations.threeMs){ scoring.push(['m', 'm', 'm']); } // better way of adding to the array
        if (combinations.threeLs){ scoring.push(['l', 'l', 'l']); }
        if (combinations.threeCs){ scoring.push(['c', 'c', 'c']); }
        if (combinations.threeDs){ scoring.push(['d', 'd', 'd']); }
        if (combinations.xsOrVs){
            for (const value of ['x', 'v']){
                for (let count = 0; count < counts[value]; count++){
                    scoring.push(value);
                }
            }
        }
        return scoring.flat();
    }

    #CreateScoreMessage(combinations, currentRoll){

        let message = "";

        if (combinations.fourVs) { 
            message = "Four V's";
            return message;
        }

        if(combinations.oneOfEach){ message += "One of each. "; }
        if(combinations.sixOfAKind){ message += "Six of a kind. "; }
        if(combinations.threePairs){ message += "Three pairs. "; }
        if(combinations.threeMs){ message += "Three M's. "; }
        if(combinations.threeDs){ message += "Three D's. "; }
        if(combinations.threeCs){ message += "Three C's. "; }
        if(combinations.threeLs){ message += "Three L's. "; }
        if(combinations.xsOrVs){
            const counts = this.#CountValues(currentRoll);
            if(counts.x > 0){
                const xMessage = counts.x === 1 ? "1 X. " : `${counts.x} X's. `;
                message += xMessage;
            }
            if(counts.v > 0){
                const vMessage = counts.v === 1 ? "1 V. " : `${counts.v} V's. `;
                message += vMessage;
            }
        }
        return message;
    }

    #CalculateScoreFromCombinations(diceArray){

        let rollScore = 0;

        if(this.#combinations.fourVs) { return rollScore; }

        if (diceArray.length = 6){
            if (this.#combinations.sixOfAKind){
                rollScore = 5000;
                return rollScore;
            }
            if (this.#combinations.oneOfEach){
                rollScore = 2000;
                return rollScore;
            }
            if (this.#combinations.threePairs){
                rollScore = 1000;
                return rollScore;
            }
        }

        if (this.#combinations.threeMs){
            rollScore = 1000;
        }
        if (this.#combinations.threeDs){
            rollScore += 500;
        }
        if (this.#combinations.threeCs){
            rollScore += 100;   
        }
        if (this.#combinations.threeLs){
            rollScore += 50;
        }
        if (this.#combinations.xsOrVs){
            rollScore += diceArray.filter(value => value === dieFaces.x).length * 10 + diceArray.filter(value => value === dieFaces.v).length * 5;
        }
        return rollScore;
    }

    #CountValues(diceArray){
        let counts = {
            'v': 0,
            'x': 0,
            'l': 0,
            'c': 0,
            'd': 0,
            'm': 0
        };
        diceArray.forEach(value => counts[value]++) // what happens if the input array contains entries that are not in the counts object?
        return counts;
    }

    ThreeMs(diceArray){
        return diceArray.filter(value => value === dieFaces.m).length >= 3
    }

    ThreeDs(diceArray){
        return diceArray.filter(value => value === dieFaces.d).length >= 3
    }

    ThreeCs(diceArray){
        return diceArray.filter(value => value === dieFaces.c).length >= 3
    }

    ThreeLs(diceArray){
        return diceArray.filter(value => value === dieFaces.l).length >= 3
    }
}

export { ScoreChecker } 