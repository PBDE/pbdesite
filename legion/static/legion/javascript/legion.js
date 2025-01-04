'use-strict';

const rollButton = document.querySelector('#roll-btn');
const endButton = document.querySelector('#end-btn');
const soloButton = document.querySelector('#solo-btn');
const pandpButton = document.querySelector('#pandp-btn');
const aiButton = document.querySelector('#ai-btn');
const playerNumberText = document.querySelector('#player-number');
const totalScoreText = document.querySelector('#total-score');
const rollScoreText = document.querySelector('#roll-score');
const keepingScoreText = document.querySelector('#keeping-score');
const diceElements = document.querySelectorAll('.die');
const rollMessage = document.querySelector('.roll-message');

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
    #activePlayer;
    #scoreChecker;
    #scoreResult;
    #rollScore = 0;
    #scoringDiceAvailable = [];

    constructor(playerCount, versesAI){

        this.#scoreChecker = new ScoreChecker();

        if (!versesAI){
            for(let i = 0; i < playerCount; i++) {
                const player = new Player(i + 1);
                this.#players.push(player);
            }
        }
        else {
            // create one player and add it to #players
            // create one ai player and add it to #players
        }
        this.#activePlayer = this.#players[0];
        playerNumberText.textContent = this.#activePlayer.GetPlayerID();

        for (let i = 0; i < diceElements.length; i ++) {
            const die_id = `die-${i + 1}`;
            const die = new Die (die_id, this);
            this.#dieInstances[die_id] = die;
        }

        rollButton.addEventListener('click', this.#Roll.bind(this));
        endButton.addEventListener('click', this.#EndTurn.bind(this));
        endButton.disabled = true;
    }

    KeepingContainsScoringCombination(){

        // must also check that keeping contains only full scoring combinations
        // currently if three pairs are rolled a roll is allowed if one of the kept die is an x or v even if a single c is kept, rather than both c's that
        // roll is also allowed if three of a kind and an x are rolled and the x is kept then one of the three of a kinds is kept

        const keeping = this.#KeepingDice();
        const keepingCombinations = this.#scoreChecker.CheckCombinations(keeping);
        if(Object.values(keepingCombinations).includes(true)){
            rollButton.disabled = false; 
        }
        else {
            rollButton.disabled = true;
        }
    }

    GetScoringDiceAvailable(){
        return this.#scoringDiceAvailable;
    }

    #Roll(){
        rollButton.disabled = true;
        let currentRoll = [];

        Object.values(this.#dieInstances).forEach(die => currentRoll.push(die.Roll()));
        this.#scoreResult = this.#scoreChecker.CheckScore(currentRoll);
        this.#rollScore = this.#scoreResult.rollScore;
        this.#scoringDiceAvailable = this.#ScoringDiceAvailable();

        endButton.disabled = false;
        rollScoreText.textContent = this.#rollScore;
        
        if (this.#scoringDiceAvailable.length === 0){

            const message = this.#scoreResult.combinations.fourVs ? this.#scoreResult.rollMessage : "No score. Turn Over";

            rollMessage.textContent = message;
            this.#UpdateRollScore(0);
            
        }
        else {
            console.log(this.#scoreResult.rollMessage);
            rollMessage.textContent = this.#scoreResult.rollMessage;
        }
    }
    
    #EndTurn(){
        this.#NextPlayer();
        this.#UpdateRollScore(0);
        Object.values(this.#dieInstances).forEach(die => die.Reset());
        rollButton.disabled = false;
        endButton.disabled = true;
    }

    #ScoringDiceAvailable(){
        const alreadyKept = [...this.#KeptDice(), ...this.#KeepingDice()];
        const availableToKeep = [...this.#scoreResult.scoring];

        // remove the dice that have already been kept from availableToKeep
        alreadyKept.forEach(function(value){
            const index = availableToKeep.indexOf(value);
            if (index > -1){ availableToKeep.splice(index, 1); }
        });
        return availableToKeep;
    }

    #KeptDice(){
        let kept = [];
        Object.values(this.#dieInstances).forEach(function(die){
            if (die.kept){ kept.push(die.value); }
        });
        return kept;
    }

    #KeepingDice(){
        let keeping = [];
        Object.values(this.#dieInstances).forEach(function(die){
            if (die.keeping){ keeping.push(die.value); }
        });
        return keeping;
    }

    #NextPlayer(){
        this.#activePlayer.SetTotalScore(this.#rollScore);
        let playerindex = this.#activePlayer.GetPlayerID();
        if (playerindex >= this.#players.length){ playerindex = 0; }
        this.#activePlayer = this.#players[playerindex];
        playerNumberText.textContent = this.#activePlayer.GetPlayerID()
        totalScoreText.textContent = this.#activePlayer.GetTotalScore();
    }

    #UpdateRollScore(score){
        this.#rollScore = score;
        rollScoreText.textContent = this.#rollScore;
    }
}

class Player {

    #playerID;
    #totalScore = 0;

    constructor(playerID) {
        this.#playerID = playerID;
    }

    GetPlayerID(){
        return this.#playerID;
    }

    GetTotalScore(){
        return this.#totalScore;
    }

    SetTotalScore(score){
        this.#totalScore += score;
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

    Reset(){
        this.kept = false;
        this.keeping = false;
        this.#element.style.backgroundColor = 'purple';
    }

    #DiePressed(){

        console.clear();

        if(this.kept){
            console.log(`${this.#dieElementID} already kept`);
        }
        else if(this.keeping || this.#gameManager.GetScoringDiceAvailable().includes(this.value)) {
            this.keeping = !this.keeping;
            this.#element.style.backgroundColor = this.keeping ? 'red' : 'purple';
        }
        else {
            console.log(`${this.#dieElementID} can't be kept`);
        }
        this.#gameManager.KeepingContainsScoringCombination();

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
            'threeMs': diceArray.filter(value => value === dieFaces.m).length >= 3,
            'threeDs': diceArray.filter(value => value === dieFaces.d).length >= 3,
            'threeCs': diceArray.filter(value => value === dieFaces.c).length >= 3,
            'threeLs': diceArray.filter(value => value === dieFaces.l).length >= 3,
            'fourVs': diceArray.filter(value => value === dieFaces.v).length >= 4,
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
}

class App {

    constructor() {    
        
        const isPassAndPlay = true;
        const isVersesAI = true;

        soloButton.addEventListener('click', this.#StartGame.bind(this, !isPassAndPlay, !isVersesAI));
        pandpButton.addEventListener('click', this.#StartGame.bind(this, isPassAndPlay, !isVersesAI));
        aiButton.addEventListener('click', this.#StartGame.bind(this, !isPassAndPlay, isVersesAI));
    }

    #PlayerCount() {

        // implement get player count
        return 2;
    }

    #StartGame(passAndPlay, versesAI) {

        // could use a switch statement based on the id of the button clicked rather than passing the arguement in

        let playerCount = 1;
        if (passAndPlay) playerCount = this.#PlayerCount();
        if (versesAI) playerCount = 2;
        this.GameManager = new GameManager(playerCount, versesAI);
        this.#HideGameButtons();
    }

    #HideGameButtons() { // replace with a loop
        document.querySelector('.turn-btns').classList.remove('hidden');
        document.querySelector('.cont-score').classList.remove('hidden');
        document.querySelector('.mode-btns').classList.add('hidden');
    }
}

const app = new App();
