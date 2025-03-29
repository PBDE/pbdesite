// 'use-strict';

import { GameManager } from "./game_manager.js";

const soloButton = document.querySelector('#solo-btn');
// const pandpButton = document.querySelector('#pandp-btn');
// const aiButton = document.querySelector('#ai-btn');

const openRulesModalButton = document.querySelector('#rules-btn');
const closeRulesModalButton = document.querySelector('#close-modal-btn');
const rulesModal = document.querySelector('#rules-modal');

class App {

    constructor() {    
        
        const isPassAndPlay = true;
        const isVersesAI = true;

        soloButton.addEventListener('click', this.#StartGame.bind(this, !isPassAndPlay, !isVersesAI));
        // pandpButton.addEventListener('click', this.#StartGame.bind(this, isPassAndPlay, !isVersesAI));
        // aiButton.addEventListener('click', this.#StartGame.bind(this, !isPassAndPlay, isVersesAI));

        openRulesModalButton.addEventListener('click', this.#OpenRulesModal);
        closeRulesModalButton.addEventListener('click', this.#CloseRulesModal);
        rulesModal.addEventListener('click', this.#CloseAfterBackDropClick.bind(this));
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
        // rulesModal.classList.remove('hidden');
        // rulesModalOverlay.classList.remove('hidden');
        rulesModal.showModal();
    }
    
    #CloseRulesModal(){
        // rulesModal.classList.add('hidden');
        // rulesModalOverlay.classList.add('hidden');
        rulesModal.close();
    }

    #CloseAfterBackDropClick(event){
        let rect = event.target.getBoundingClientRect();
      
        // console.log(
        //             `
        //             ClientX: ${event.clientX}
        //             rect.left: ${rect.left}
        //             rect.right: ${rect.right}
  
        //             ClientY: ${event.clientY}
        //             rect.top: ${rect.left}
        //             rect.bottom: ${rect.bottom}
        //             `
        //            );

          if (
            rect.left > event.clientX || 
            rect.right < event.clientX ||
            rect.top > event.clientY ||
            rect.bottom < event.clientY)
            {
                this.#CloseRulesModal();
            }
    }
}

const app = new App();
