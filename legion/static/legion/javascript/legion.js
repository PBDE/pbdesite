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
    #isFirstRoll = true;
    #scoreChecker;
    #activePlayer;
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
        const availableToKeep = [...this.#scoreResult.scoring].flat();

        alreadyKept.forEach(function(value){
            const index = availableToKeep.indexOf(value);
            if (index > -1){ availableToKeep.splice(index, 1); }
        });

        // availableToKeep shouldn't be flat as it will be needed when checking if a scoring dice combination has been kept before a new roll
        
        console.clear()
        console.log("Scoring");
        console.log(this.#scoreResult.scoring);
        console.log("Already kept");
        console.log(alreadyKept);
        console.log("Available to keep");
        console.log((availableToKeep));

        if(availableToKeep.length === 0){
            console.log("No scoring");
        }
        
        return availableToKeep;
    }

    #keepingContainsScoringCombination(){
        const keeping = this.#getKeepingDice();
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

    #Roll(){
        let currentRoll = [];
        Object.values(this.#dieInstances).forEach(die => currentRoll.push(die.Roll()));
        this.#scoreResult = this.#scoreChecker.CheckScore(currentRoll, this.#isFirstRoll);
        this.#isFirstRoll = false;

        // disable the roll button
            // remove event listener
            // grey out button
            
        // after a die is clicked - check if a roll is allowed
    }

    #EndTurn(){
        console.log("End Turn");
        this.#isFirstRoll = true;

        // add the score to the player's score
        // move to the next player
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
    }
}

class ScoreChecker {

    #counts;
    #currentRoll;
    #scoring;
    
    CheckScore(currentRoll, isFirstRoll){

        this.#counts = {
            'v': 0,
            'x': 0,
            'l': 0,
            'c': 0,
            'd': 0,
            'm': 0
        };
        this.#scoring = []
        this.#currentRoll = currentRoll;
        this.#checkCombinations(isFirstRoll); // pass optionsToKeep in then return it

        return { scoring: this.#scoring }
    }

    #checkCombinations(isFirstRoll){

        this.#currentRoll.forEach(roll => this.#counts[roll]++);

        if (this.#OneOfEach()){
            console.log("One of each");
            this.#scoring.push(this.#currentRoll);
        }

        if (this.#SixOfAKind()){
            console.log("Six of a kind");
            this.#scoring.push(this.#currentRoll);
        }
        
        if (this.#ThreePairs()){
            console.log("Three pairs");
            this.#scoring.push(this.#currentRoll);
        }

        if (this.#ThreeMs()){
            console.log("3 M's");
            this.#scoring.push(['m', 'm', 'm']);
            // this.#AddToScoringArray(dieFaces.m)
        }

        if (this.#ThreeLs()){
            console.log("3 L's");
            this.#scoring.push(['l', 'l', 'l']);
        }

        if (this.#ThreeCs()){
            console.log("3 C's");
            this.#scoring.push(['c', 'c', 'c']);
        }

        if (this.#ThreeDs()){
            console.log("3 D's");
            this.#scoring.push(['d', 'd', 'd']);
        }

        if (this.#FourVs()){
            console.log("4 V's")
        }
        
        for (const value of ['x', 'v']){
            for (let count = 0; count < this.#counts[value]; count++){
                this.#scoring.push(value);
            }
        }

        if (isFirstRoll){
            
            if (this.#AllNoScoring()){
                console.log("No scoring");
            }
            
            if (this.#AllScoring()){
                console.log("All scoring");
            }
        }
    }

    // #AddToScoringArray(value){
    //     for (let i = 0; i < 3; i++){
    //         if (this.scoring.length < 6) {
    //             this.#scoring.push(value);
    //         }
    //     }
    // }

    #AllNoScoring(){
        return this.#scoring.length === 0;
    }

    #AllScoring(){
        return this.#scoring.flat().length === 6; // all scoring doesn't work with 3 of a kind plus 3 x's or v's
    }

    #OneOfEach(){
        return Object.values(this.#counts).every(count => count === 1);
    }

    #SixOfAKind(){
        return this.#currentRoll.every(value => value === this.#currentRoll[0]);
    }

    #ThreePairs(){
        let pairsCount = 0
        Object.values(this.#counts).forEach(function(count){
            if (count === 2) pairsCount ++;
            if (count === 4) pairsCount += 2;
        })
        return pairsCount === 3;
    }

    #ThreeMs(){
        return this.#counts['m'] >= 3;
    }

    #ThreeDs(){
        return this.#counts['d'] >= 3;
    }

    #ThreeCs(){
        return this.#counts['c'] >= 3;
    }

    #ThreeLs(){
        return this.#counts['l'] >= 3;
    }
    
    #FourVs(){
        return this.#counts['v'] >= 4;
    }
}

class App {

    #isPassAndPlay = true;
    #isVersesAI = true;

    constructor() {        
        soloButton.addEventListener('click', this.#startGame.bind(this, !this.#isPassAndPlay, !this.#isVersesAI));
        pandpButton.addEventListener('click', this.#startGame.bind(this, this.#isPassAndPlay, !this.#isVersesAI));
        aiButton.addEventListener('click', this.#startGame.bind(this, !this.#isPassAndPlay, this.#isVersesAI));
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
