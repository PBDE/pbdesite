
import { ScoreChecker } from "./score_checker.js";
import { Player } from "./player.js";
import { Die } from "./die.js";
import { dieFaces } from "./support.js";

const rollButton = document.querySelector('#roll-btn');
const endButton = document.querySelector('#end-btn');
// const playerNumberText = document.querySelector('#player-number');
const totalScoreText = document.querySelector('#total-score');
const rollScoreText = document.querySelector('#roll-score');
const keepingScoreText = document.querySelector('#keeping-score');
const diceElements = document.querySelectorAll('.die');
const rollMessage = document.querySelector('.roll-message');

class GameManager {

    #dieInstances = {};
    #players = [];
    #activePlayer;
    #scoreChecker;
    #scoreResult;
    #rollScore = 0;
    #scoringDiceAvailable = [];
    #messageHidden = true;

    constructor(playerCount, versesAI){

        this.#scoreChecker = new ScoreChecker();

        if (!versesAI){
            for(let i = 0; i < playerCount; i++) {
                const player = new Player(i + 1);
                this.#players.push(player);
            }
        }
        // else {
        //     create one player and add it to #players
        //     create one ai player and add it to #players
        // }
        this.#activePlayer = this.#players[0];
        // playerNumberText.textContent = this.#activePlayer.GetPlayerID();

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

        const keeping = this.#KeepingDice();
        const keepingCombinations = this.#scoreChecker.CheckCombinations(keeping);

        const CheckThreeMsDsCsLs = function(keeping, scoreChecker){
            let threekept = true;
            if (keeping.includes(dieFaces.m)){
                if (!scoreChecker.ThreeMs(keeping)) { threekept = false; }
            }
            if (keeping.includes(dieFaces.d)){
                if (!scoreChecker.ThreeDs(keeping)) { threekept = false; }
            }
            if (keeping.includes(dieFaces.c)){
                if (!scoreChecker.ThreeCs(keeping)) { threekept = false; }
            }
            if (keeping.includes(dieFaces.l)){
                if (!scoreChecker.ThreeLs(keeping)) { threekept = false; }
            }
            return threekept;
        }
        if(Object.values(keepingCombinations).includes(true) && CheckThreeMsDsCsLs(keeping, this.#scoreChecker)){
            rollButton.disabled = false; 
        }
        else {
            rollButton.disabled = true;
        }
    }

    UpdateKeepingScore(){
        if(this.#KeepingDice().length === 0) {
            keepingScoreText.textContent = this.#rollScore;
        }
        else{
            const keepingOrKept = [...this.#KeepingDice(), ...this.#KeptDice()];
            const keepingScore = this.#scoreChecker.CalculateScoreIncompleteArray(keepingOrKept);
            keepingScoreText.textContent = keepingScore;
        }
    }

    GetScoringDiceAvailable(){
        return this.#scoringDiceAvailable;
    }

    #Roll(){
        rollButton.disabled = true;
        let currentRoll = [];

        if(this.#messageHidden) {
            document.querySelector('.cont-message').classList.remove('invisible');
            this.#messageHidden = false;
        }

        Object.values(this.#dieInstances).forEach(die => currentRoll.push(die.Roll()));
        this.#scoreResult = this.#scoreChecker.CheckScore(currentRoll);
        this.#rollScore = this.#scoreResult.rollScore;
        this.#scoringDiceAvailable = this.#ScoringDiceAvailable();

        endButton.disabled = false;
        rollScoreText.textContent = this.#rollScore;
        this.UpdateKeepingScore();
        
        if(this.#scoringDiceAvailable.length === 0){
            const message = this.#scoreResult.combinations.fourVs ? this.#scoreResult.rollMessage : "No score. Turn Over";
            rollMessage.textContent = message;
            keepingScoreText.textContent = 0;
            this.#UpdateRollScore(0);
            Object.values(this.#dieInstances).forEach(die => die.Reset());
        }
        else{
            rollMessage.textContent = this.#scoreResult.rollMessage;
        }
        if(this.#scoreResult.combinations.fourVs){
            this.#activePlayer.SetTotalToZero();
            totalScoreText.textContent = this.#activePlayer.GetTotalScore();
        }
    }
    
    #EndTurn(){
        this.#NextPlayer();
        this.#UpdateRollScore(0);
        Object.values(this.#dieInstances).forEach(die => die.Reset());
        rollButton.disabled = false;
        endButton.disabled = true;
        keepingScoreText.textContent = 0;
    }

    #ScoringDiceAvailable(){
        const alreadyKept = [...this.#KeptDice(), ...this.#KeepingDice()];
        const availableToKeep = [...this.#scoreResult.scoring];

        // remove the dice that have already been kept from the availableToKeep array
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
        // playerNumberText.textContent = this.#activePlayer.GetPlayerID()
        totalScoreText.textContent = this.#activePlayer.GetTotalScore();
    }

    #UpdateRollScore(score){
        this.#rollScore = score;
        rollScoreText.textContent = this.#rollScore;
    }
}

export { GameManager };