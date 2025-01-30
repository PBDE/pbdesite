
import { dieFaces } from "./support";

class Die {

    kept = false;
    keeping = false;
    locked = false;
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

        if(this.locked){ this.locked = false; }

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
        this.locked = true;
        this.kept = false;
        this.keeping = false;
        this.#element.style.backgroundColor = 'purple';
    }

    #DiePressed(){

        if(this.locked === true){ return; }

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

export { Die }