
import { dieFaces } from "./support";

class Die {

    kept = false;
    keeping = false;
    locked = true;
    value;
    #dieElementID;
    #element;
    #gameManager;
    #faces = Object.values(dieFaces);
    #baseColour;
    #keepingColour;
    #keptColour;

    constructor(dieElementID, gameManager){
        this.#dieElementID = dieElementID;
        this.#gameManager = gameManager;
        this.#element = document.getElementById(`${this.#dieElementID}`);
        this.#element.addEventListener('click', this.#DiePressed.bind(this));

        this.#baseColour = getComputedStyle(document.documentElement).getPropertyValue('--dice-base-colour');
        this.#keepingColour = getComputedStyle(document.documentElement).getPropertyValue('--dice-keeping-colour');
        this.#keptColour = getComputedStyle(document.documentElement).getPropertyValue('--dice-kept-colour');
    }

    Roll(){

        if(this.locked){ this.locked = false; }
        this.#EnableDie();

        if (!this.keeping && !this.kept) {
            this.value = this.#faces[Math.floor(Math.random() * this.#faces.length)];
            this.#element.textContent = this.value;
        }
        if (this.keeping){
            this.kept = true;
            this.keeping = false;
            this.#element.style.backgroundColor = this.#keptColour;
        }
        return this.value;
    }

    Reset(){
        this.locked = true;
        this.kept = false;
        this.keeping = false;
        this.#element.style.backgroundColor = this.#baseColour;
        this.#DisableDie();
    }

    #DisableDie(){
        this.#element.disabled = true;
    }

    #EnableDie(){
        this.#element.disabled = false;
    }

    #DiePressed(){

        if(this.locked === true){ return; }

        if(this.keeping || this.#gameManager.GetScoringDiceAvailable().includes(this.value)) {
            this.keeping = !this.keeping;
            this.#element.style.backgroundColor = this.keeping ? this.#keepingColour : this.#baseColour;
        }
        this.#gameManager.KeepingContainsScoringCombination();
        this.#gameManager.UpdateKeepingScore();

        // check if all dice have been kept - roll button should become unavailable
    }
}

export { Die }