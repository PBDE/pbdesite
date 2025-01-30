// 'use-strict';

import { GameManager } from "./game_manager.js";

const soloButton = document.querySelector('#solo-btn');
const pandpButton = document.querySelector('#pandp-btn');
const aiButton = document.querySelector('#ai-btn');

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
