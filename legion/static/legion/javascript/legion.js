'use-strict';

const rollButton = document.querySelector('#roll-btn');
const endButton = document.querySelector('#end-btns');
const soloButton = document.querySelector('#solo-btn');
const pandpButton = document.querySelector('#pandp-btn');
const aiButton = document.querySelector('#ai-btn');
const totalScoreDisplay = document.querySelector('#total-score');
const currentScoreDisplay = document.querySelector('#current-score');
const diceElements = document.querySelectorAll('.die');

const dieFaces = {
    v: 'v',
    x: 'x',
    l: 'l',
    c: 'c',
    d: 'd',
    m: 'm'
}

class GameManager {

    #dieInstances = {};
    #players = [];
    #scoreChecker;
    #scoreResult;

    constructor(playerCount, versesAI){

        this.#scoreChecker = new ScoreChecker();

        if (!versesAI){
            for(let i = 0; i < playerCount; i++) {
                const player = new Player(`Player ${i + 1}`);
                this.#players.push(player);
            }
        }
        else {
            // create one player and add it to #players
            // create one ai player and add it to #players
        }

        for (let i = 0; i < diceElements.length; i ++) {
            const die_id = `die-${i + 1}`;
            const die = new Die (die_id, this);
            this.#dieInstances[die_id] = die;
        }

        rollButton.addEventListener('click', this.#Roll.bind(this));
        endButton.addEventListener('click', this.#EndTurn);
    }
    
    getScoringDiceAvailable(){

        const alreadyKept = [...this.#getKeptDice(), ...this.#getKeepingDice()];
        const availableToKeep = [...this.#scoreResult.scoring];

        // remove the dice that have already been kept from availableToKeep
        alreadyKept.forEach(function(value){
            const index = availableToKeep.indexOf(value);
            if (index > -1){ availableToKeep.splice(index, 1); }
        });

        // console.clear()
        // console.log("Scoring");
        // console.log(this.#scoreResult.scoring);
        // console.log("Already kept");
        // console.log(alreadyKept);
        // console.log("Available to keep");
        // console.log((availableToKeep));

        if(availableToKeep.length === 0){
            console.log("No score. Roll over");
        }
        
        return availableToKeep;
    }

    keepingContainsScoringCombination(){

        // must also check that keeping contains only full scoring combinations
        // currently if three pairs are rolled a roll is allowed if one of the kept die is an x or v even if a single c is kept, rather than both c's that

        const keeping = this.#getKeepingDice();

        console.log("Keeping:");
        console.log(keeping);
        
        const keepingCombinations = this.#scoreChecker.CheckCombinations(keeping);

        console.log("Keeping combinations:");
        console.log(keepingCombinations);

        if(Object.values(keepingCombinations).includes(true)){
            rollButton.disabled = false; 
        }
        else {
            rollButton.disabled = true;
        }
    }

    #Roll(){
        let currentRoll = [];
        Object.values(this.#dieInstances).forEach(die => currentRoll.push(die.Roll()));
        this.#scoreResult = this.#scoreChecker.CheckScore(currentRoll);
        console.log("Roll Score: ");
        console.log(this.#scoreResult.rollScore);
        rollButton.disabled = true;
    }
    
    #EndTurn(){
        console.log("End Turn");

        // add the score to the player's score
        // move to the next player
    }

    #getKeptDice(){
        let kept = [];
        Object.values(this.#dieInstances).forEach(function(die){
            if (die.kept){ kept.push(die.value); }
        });
        return kept;
    }

    #getKeepingDice(){
        let keeping = [];
        Object.values(this.#dieInstances).forEach(function(die){
            if (die.keeping){ keeping.push(die.value); }
        });
        return keeping;
    }
}

class Player {

    #playerID; 

    constructor(playerID) {
        this.#playerID = playerID;
    }
}

class Die {

    kept = false;
    keeping = false;
    value;
    #dieElementID;
    #element;
    #gameManager;
    #faces = Object.values(dieFaces);

    constructor(dieElementID, gameManager){
        this.#dieElementID = dieElementID;
        this.#gameManager = gameManager;
        this.#element = document.getElementById(`${this.#dieElementID}`);
        this.#element.addEventListener('click', this.#DiePressed.bind(this));
    }

    Roll(){
        if (!this.keeping && !this.kept) {
            this.value = this.#faces[Math.floor(Math.random() * this.#faces.length)];
            this.#element.textContent = this.value;
        }
        if (this.keeping){
            this.kept = true;
            this.keeping = false;
            this.#element.style.backgroundColor = 'blue';
        }
        return this.value;
    }

    #DiePressed(){

        console.clear();

        if(this.kept){
            console.log(`${this.#dieElementID} already kept`);
        }
        else if(this.keeping || this.#gameManager.getScoringDiceAvailable().includes(this.value)) {
            this.keeping = !this.keeping;
            this.#element.style.backgroundColor = this.keeping ? 'red' : 'purple';
        }
        else {
            console.log(`${this.#dieElementID} can't be kept`);
        }
        this.#gameManager.keepingContainsScoringCombination();

        // calculate keeping score

        // check if all dice have been kept - roll button should become unavailable
    }
}

class ScoreChecker {

    #combinations;

    CheckScore(currentRoll){

        this.#combinations = this.CheckCombinations(currentRoll);
        const scoring = this.#CreateScoringArray(this.#combinations, currentRoll);
        const rollScore = this.#CalculateScoreFromCombinations(currentRoll);

        return { scoring: scoring, combinations: this.#combinations, rollScore: rollScore }
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
            'sixOfAKind': diceArray.every(value => value === diceArray[0]),
            'oneOfEach': Object.values(counts).every(value => value === 1),
            'threePairs': ThreePairs(counts),
            'threeMs': diceArray.filter(value => value === dieFaces.m).length >= 3,
            'threeDs': diceArray.filter(value => value === dieFaces.d).length >= 3,
            'threeCs': diceArray.filter(value => value === dieFaces.c).length >= 3,
            'threeLs': diceArray.filter(value => value === dieFaces.l).length >= 3,
            'xsOrVs': diceArray.includes(dieFaces.v) || diceArray.includes(dieFaces.x)
        }
        return combinations;
    }

    CalculateScoreIncompleteArray(diceArray){ // too much repitition - create a three of a kind method

        let score = 0;

        if (diceArray.filter(value => value === dieFaces.m).length >= 3){
            score = 1000;
        }
        if (diceArray.filter(value => value === dieFaces.d).length >= 3){
            score += 500;
        }
        if (diceArray.filter(value => value === dieFaces.c).length >= 3){
            score += 100;
        }
        if (diceArray.filter(value => value === dieFaces.l).length >= 3){
            score += 50;
        }
        score += diceArray.filter(value => value === dieFaces.x).length * 10;
        score += diceArray.filter(value => value === dieFaces.v).length * 5;
        return score;
    }

    #CreateScoringArray(combinations, currentRoll){

        const counts = this.#CountValues(currentRoll);

        let scoring = []
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

    #CalculateScoreFromCombinations(diceArray){

        let rollScore = 0;

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
}

class App {

    constructor() {    
        
        const isPassAndPlay = true;
        const isVersesAI = true;

        soloButton.addEventListener('click', this.#startGame.bind(this, !isPassAndPlay, !isVersesAI));
        pandpButton.addEventListener('click', this.#startGame.bind(this, isPassAndPlay, !isVersesAI));
        aiButton.addEventListener('click', this.#startGame.bind(this, !isPassAndPlay, isVersesAI));
    }

    #getPlayerCount() {

        // implement get player count
        return 2;
    }

    #startGame(passAndPlay, versesAI) {

        // could use a switch statement based on the id of the button clicked rather than passing the arguement in

        let playerCount = 1;
        if (passAndPlay) playerCount = this.#getPlayerCount();
        if (versesAI) playerCount = 2;
        this.GameManager = new GameManager(playerCount, versesAI);
        this.#hideGameButtons();
    }

    #hideGameButtons() {
        document.querySelector('.turn-btns').classList.remove('hidden');
        document.querySelector('.cont-score').classList.remove('hidden');
        document.querySelector('.mode-btns').classList.add('hidden');
    }
}

const app = new App();
