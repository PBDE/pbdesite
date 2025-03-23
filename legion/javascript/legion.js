// 'use-strict';

import { GameManager } from "./game_manager.js";

const soloButton = document.querySelector('#solo-btn');
// const pandpButton = document.querySelector('#pandp-btn');
// const aiButton = document.querySelector('#ai-btn');
const rulesModalButton = document.querySelector('#rules-btn');
const closeModalButton = document.querySelector('#close-modal-btn');
const rulesModal = document.querySelector('#rules-modal');
const rulesModalOverlay = document.querySelector('#overlay');


class App {

    constructor() {    
        
        const isPassAndPlay = true;
        const isVersesAI = true;

        soloButton.addEventListener('click', this.#StartGame.bind(this, !isPassAndPlay, !isVersesAI));
        // pandpButton.addEventListener('click', this.#StartGame.bind(this, isPassAndPlay, !isVersesAI));
        // aiButton.addEventListener('click', this.#StartGame.bind(this, !isPassAndPlay, isVersesAI));

        rulesModalButton.addEventListener('click', this.#OpenRulesModal);
        closeModalButton.addEventListener('click', this.#CloseRulesModal);
        rulesModalOverlay.addEventListener('click', this.#CloseRulesModal);

        document.addEventListener('keydown', this.#EscapeModal.bind(this));
    }

    #PlayerCount() {

        // implement get player count
        return 2;
    }

    #StartGame(passAndPlay, versesAI) {

        let playerCount = 1;
        if (passAndPlay) playerCount = this.#PlayerCount();
        if (versesAI) playerCount = 2;
        this.GameManager = new GameManager(playerCount, versesAI);
        this.#HideGameButtons();
    }

    #HideGameButtons() {
        document.querySelector('.cont-score').classList.remove('invisible');
        document.querySelector('.turn-btns').classList.remove('hidden');
        document.querySelector('.mode-btns').classList.add('hidden');
    }

    #OpenRulesModal() {
        rulesModal.classList.remove('hidden');
        rulesModalOverlay.classList.remove('hidden');
    }

    #EscapeModal(event){
        if (event.key === 'Escape' && !rulesModal.classList.contains('hidden'))
            {
                this.#CloseRulesModal(); 
            }
    }

    #CloseRulesModal(){
        rulesModal.classList.add('hidden');
        rulesModalOverlay.classList.add('hidden');
    }

}

const app = new App();
