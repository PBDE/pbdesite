
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

    SetTotalToZero(){
        this.#totalScore = 0;
    }

    SetTotalScore(score){
        this.#totalScore += score;
    }
}

export { Player }