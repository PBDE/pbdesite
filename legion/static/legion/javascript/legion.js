'use-strict';

const rollButton = document.querySelector('#roll-btn');
const endButton = document.querySelector('#end-btns');
const soloButton = document.querySelector('#solo-btn');
const pandpButton = document.querySelector('#pandp-btn');
const aiButton = document.querySelector('#ai-btn');

const totalScoreDisplay = document.querySelector('#total-score');
const currentScoreDisplay = document.querySelector('#current-score');

const diceElements = document.querySelectorAll('.die');

class GameManager {

    #diceInstances = {};
    #players = [];

    constructor(playerCount, versesAI){

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
            const die = new Die (die_id);
            this.#diceInstances[die_id] = die;
        }

        console.log(this.#diceInstances);

        diceElements.forEach(function(diceElement) {
            diceElement.addEventListener('click', this.#DicePressed);
        }, this);

        rollButton.addEventListener('click', this.#Roll.bind(this));
        endButton.addEventListener('click', this.#EndTurn);

        const scoreChecker = new ScoreChecker();
    }

    #SetPlayer() {
        // modal that asks for the number of players
    }

    #DicePressed(){
        console.log("Dice pressed");
    }

    #Roll(){

        for (const [key, die] of Object.entries(this.#diceInstances)){
            die.Roll();
        }        
    }

    #EndTurn(){
        console.log("End Turn");

        // add the score to the player's score
        // move to the next player
    }
}

class Player {

    #playerID; 

    constructor(playerID) {
        this.#playerID = playerID
    }
}

class Die {

    #scoring = false;
    #kept = false;
    #keeping = false;
    #faces = ['V', 'X', 'L', 'C', 'D', 'M'];
    
    value = this.#faces[0];

    constructor(dieElementID){
        
        this.dieElementID = dieElementID;
    }

    Roll(){
        console.log(`Rolled ${this.dieElementID}`);
        this.value = this.#faces[Math.floor(Math.random() * this.#faces.length)];
        console.log(this.value);

        // document.getElementById(`#${this.dieElementID}`).textContent = this.#value;
    }

    // set scoring
    // get scoring
    // set kept
    // get kept
    // set keeping
    // get keeping
}

class ScoreChecker {

    #rollCounter = 0;

    constructor() {
        console.log("score counter");
    }

    CheckScore(){

    }

    #CheckAllNoScoring(){

    }

    #CheckAllScoring(){

    }

    #CheckMinimumScore(){

    }

    #CheckNewRolledScoring(){

    }

    #CheckCircus(){

    }

    #CheckSixOfAKind(){

    }

    #CheckThreePairs(){

    }

    #CheckThreeOfAKind(){

    }

    #CheckX(){

    }

    #CheckV(){

    }
}

class App {

    constructor() {        
        
        // soloButton.addEventListener('click', this.#test);
        
        // soloButton.addEventListener('click', function(){
        //     const playerCount = 1;
        //     const versesAI = false;

        //     // call startGame - passing this, playerCount and versesAI - how do you pass this
        
        // });
        
        soloButton.addEventListener('click', this.#startGame.bind(this, 1, false));
        pandpButton.addEventListener('click', this.#getPlayerCount.bind(this));
        aiButton.addEventListener('click', this.#startGame.bind(this, 2, true));
    }

    // #test() {
    //     console.log(this);
    //     console.log(this.id);

    //     let playerCount = 1;
    //     let versesAI = false;

    //     if (this.id === "pandp-btn")
    //     {
    //         playerCount = this.#getPlayerCount();
    //     }

    //     if (this.id === "ai-btn")
    //     {
    //         playerCount = 2;
    //         versesAI
    //     }

    //     this.#startGame(); // this will be the HTMLElement
    // }

    #getPlayerCount() {

        // implement get player count

        this.#startGame(2, false);
    }

    #startGame(playerCount, versesAI) {
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
