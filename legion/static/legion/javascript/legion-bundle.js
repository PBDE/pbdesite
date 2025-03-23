/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./javascript/die.js":
/*!***************************!*\
  !*** ./javascript/die.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   Die: () => (/* binding */ Die)\n/* harmony export */ });\n/* harmony import */ var _support__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./support */ \"./javascript/support.js\");\n\r\n\r\n\r\nclass Die {\r\n\r\n    kept = false;\r\n    keeping = false;\r\n    locked = false;\r\n    value;\r\n    #dieElementID;\r\n    #element;\r\n    #gameManager;\r\n    #faces = Object.values(_support__WEBPACK_IMPORTED_MODULE_0__.dieFaces);\r\n    #baseColour;\r\n    #keepingColour;\r\n    #keptColour;\r\n\r\n    constructor(dieElementID, gameManager){\r\n        this.#dieElementID = dieElementID;\r\n        this.#gameManager = gameManager;\r\n        this.#element = document.getElementById(`${this.#dieElementID}`);\r\n        this.#element.addEventListener('click', this.#DiePressed.bind(this));\r\n\r\n        this.#baseColour = getComputedStyle(document.documentElement).getPropertyValue('--dice-base-colour');\r\n        this.#keepingColour = getComputedStyle(document.documentElement).getPropertyValue('--dice-keeping-colour');\r\n        this.#keptColour = getComputedStyle(document.documentElement).getPropertyValue('--dice-kept-colour');\r\n    }\r\n\r\n    Roll(){\r\n\r\n        if(this.locked){ this.locked = false; }\r\n\r\n        if (!this.keeping && !this.kept) {\r\n            this.value = this.#faces[Math.floor(Math.random() * this.#faces.length)];\r\n            this.#element.textContent = this.value;\r\n        }\r\n        if (this.keeping){\r\n            this.kept = true;\r\n            this.keeping = false;\r\n            this.#element.style.backgroundColor = this.#keptColour;\r\n        }\r\n        return this.value;\r\n    }\r\n\r\n    Reset(){\r\n        this.locked = true;\r\n        this.kept = false;\r\n        this.keeping = false;\r\n        this.#element.style.backgroundColor = this.#baseColour;\r\n    }\r\n\r\n    #DiePressed(){\r\n\r\n        if(this.locked === true){ return; }\r\n\r\n        if(this.keeping || this.#gameManager.GetScoringDiceAvailable().includes(this.value)) {\r\n            this.keeping = !this.keeping;\r\n            this.#element.style.backgroundColor = this.keeping ? this.#keepingColour : this.#baseColour;\r\n        }\r\n        this.#gameManager.KeepingContainsScoringCombination();\r\n        this.#gameManager.UpdateKeepingScore();\r\n\r\n        // check if all dice have been kept - roll button should become unavailable\r\n    }\r\n}\r\n\r\n\n\n//# sourceURL=webpack://legion/./javascript/die.js?");

/***/ }),

/***/ "./javascript/game_manager.js":
/*!************************************!*\
  !*** ./javascript/game_manager.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   GameManager: () => (/* binding */ GameManager)\n/* harmony export */ });\n/* harmony import */ var _score_checker_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./score_checker.js */ \"./javascript/score_checker.js\");\n/* harmony import */ var _player_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./player.js */ \"./javascript/player.js\");\n/* harmony import */ var _die_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./die.js */ \"./javascript/die.js\");\n/* harmony import */ var _support_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./support.js */ \"./javascript/support.js\");\n\r\n\r\n\r\n\r\n\r\n\r\nconst rollButton = document.querySelector('#roll-btn');\r\nconst endButton = document.querySelector('#end-btn');\r\n// const playerNumberText = document.querySelector('#player-number');\r\nconst totalScoreText = document.querySelector('#total-score');\r\nconst rollScoreText = document.querySelector('#roll-score');\r\nconst keepingScoreText = document.querySelector('#keeping-score');\r\nconst diceElements = document.querySelectorAll('.die');\r\nconst rollMessage = document.querySelector('.roll-message');\r\n\r\nclass GameManager {\r\n\r\n    #dieInstances = {};\r\n    #players = [];\r\n    #activePlayer;\r\n    #scoreChecker;\r\n    #scoreResult;\r\n    #rollScore = 0;\r\n    #scoringDiceAvailable = [];\r\n    #messageHidden = true;\r\n\r\n    constructor(playerCount, versesAI){\r\n\r\n        this.#scoreChecker = new _score_checker_js__WEBPACK_IMPORTED_MODULE_0__.ScoreChecker();\r\n\r\n        if (!versesAI){\r\n            for(let i = 0; i < playerCount; i++) {\r\n                const player = new _player_js__WEBPACK_IMPORTED_MODULE_1__.Player(i + 1);\r\n                this.#players.push(player);\r\n            }\r\n        }\r\n        else {\r\n            // create one player and add it to #players\r\n            // create one ai player and add it to #players\r\n        }\r\n        this.#activePlayer = this.#players[0];\r\n        // playerNumberText.textContent = this.#activePlayer.GetPlayerID();\r\n\r\n        for (let i = 0; i < diceElements.length; i ++) {\r\n            const die_id = `die-${i + 1}`;\r\n            const die = new _die_js__WEBPACK_IMPORTED_MODULE_2__.Die (die_id, this);\r\n            this.#dieInstances[die_id] = die;\r\n        }\r\n\r\n        rollButton.addEventListener('click', this.#Roll.bind(this));\r\n        endButton.addEventListener('click', this.#EndTurn.bind(this));\r\n        endButton.disabled = true;\r\n    }\r\n\r\n    KeepingContainsScoringCombination(){\r\n\r\n        const keeping = this.#KeepingDice();\r\n        const keepingCombinations = this.#scoreChecker.CheckCombinations(keeping);\r\n\r\n        const CheckThreeMsDsCsLs = function(keeping, scoreChecker){\r\n            let threekept = true;\r\n            if (keeping.includes(_support_js__WEBPACK_IMPORTED_MODULE_3__.dieFaces.m)){\r\n                if (!scoreChecker.ThreeMs(keeping)) { threekept = false; }\r\n            }\r\n            if (keeping.includes(_support_js__WEBPACK_IMPORTED_MODULE_3__.dieFaces.d)){\r\n                if (!scoreChecker.ThreeDs(keeping)) { threekept = false; }\r\n            }\r\n            if (keeping.includes(_support_js__WEBPACK_IMPORTED_MODULE_3__.dieFaces.c)){\r\n                if (!scoreChecker.ThreeCs(keeping)) { threekept = false; }\r\n            }\r\n            if (keeping.includes(_support_js__WEBPACK_IMPORTED_MODULE_3__.dieFaces.l)){\r\n                if (!scoreChecker.ThreeLs(keeping)) { threekept = false; }\r\n            }\r\n            return threekept;\r\n        }\r\n        if(Object.values(keepingCombinations).includes(true) && CheckThreeMsDsCsLs(keeping, this.#scoreChecker)){\r\n            rollButton.disabled = false; \r\n        }\r\n        else {\r\n            rollButton.disabled = true;\r\n        }\r\n    }\r\n\r\n    UpdateKeepingScore(){\r\n\r\n        const keepingOrKept = [...this.#KeepingDice(), ...this.#KeptDice()];\r\n        const keepingScore = this.#scoreChecker.CalculateScoreIncompleteArray(keepingOrKept);\r\n        keepingScoreText.textContent = keepingScore;\r\n    }\r\n\r\n    GetScoringDiceAvailable(){\r\n        return this.#scoringDiceAvailable;\r\n    }\r\n\r\n    #Roll(){\r\n        rollButton.disabled = true;\r\n        let currentRoll = [];\r\n\r\n        if(this.#messageHidden) {\r\n            document.querySelector('.cont-message').classList.remove('invisible');\r\n            this.#messageHidden = false;\r\n        }\r\n\r\n\r\n        Object.values(this.#dieInstances).forEach(die => currentRoll.push(die.Roll()));\r\n        this.#scoreResult = this.#scoreChecker.CheckScore(currentRoll);\r\n        this.#rollScore = this.#scoreResult.rollScore;\r\n        this.#scoringDiceAvailable = this.#ScoringDiceAvailable();\r\n\r\n        endButton.disabled = false;\r\n        rollScoreText.textContent = this.#rollScore;\r\n        \r\n        if(this.#scoringDiceAvailable.length === 0){\r\n            const message = this.#scoreResult.combinations.fourVs ? this.#scoreResult.rollMessage : \"No score. Turn Over\";\r\n            rollMessage.textContent = message;\r\n            keepingScoreText.textContent = 0;\r\n            this.#UpdateRollScore(0);\r\n        }\r\n        else{\r\n            rollMessage.textContent = this.#scoreResult.rollMessage;\r\n        }\r\n        if(this.#scoreResult.combinations.fourVs){\r\n            this.#activePlayer.SetTotalToZero();\r\n            totalScoreText.textContent = this.#activePlayer.GetTotalScore();\r\n        }\r\n    }\r\n    \r\n    #EndTurn(){\r\n        this.#NextPlayer();\r\n        this.#UpdateRollScore(0);\r\n        Object.values(this.#dieInstances).forEach(die => die.Reset());\r\n        rollButton.disabled = false;\r\n        endButton.disabled = true;\r\n        keepingScoreText.textContent = 0;\r\n    }\r\n\r\n    #ScoringDiceAvailable(){\r\n        const alreadyKept = [...this.#KeptDice(), ...this.#KeepingDice()];\r\n        const availableToKeep = [...this.#scoreResult.scoring];\r\n\r\n        // remove the dice that have already been kept from the availableToKeep array\r\n        alreadyKept.forEach(function(value){\r\n            const index = availableToKeep.indexOf(value);\r\n            if (index > -1){ availableToKeep.splice(index, 1); }\r\n        });\r\n        return availableToKeep;\r\n    }\r\n\r\n    #KeptDice(){\r\n        let kept = [];\r\n        Object.values(this.#dieInstances).forEach(function(die){\r\n            if (die.kept){ kept.push(die.value); }\r\n        });\r\n        return kept;\r\n    }\r\n\r\n    #KeepingDice(){\r\n        let keeping = [];\r\n        Object.values(this.#dieInstances).forEach(function(die){\r\n            if (die.keeping){ keeping.push(die.value); }\r\n        });\r\n        return keeping;\r\n    }\r\n\r\n    #NextPlayer(){\r\n        this.#activePlayer.SetTotalScore(this.#rollScore);\r\n        let playerindex = this.#activePlayer.GetPlayerID();\r\n        if (playerindex >= this.#players.length){ playerindex = 0; }\r\n        this.#activePlayer = this.#players[playerindex];\r\n        // playerNumberText.textContent = this.#activePlayer.GetPlayerID()\r\n        totalScoreText.textContent = this.#activePlayer.GetTotalScore();\r\n    }\r\n\r\n    #UpdateRollScore(score){\r\n        this.#rollScore = score;\r\n        rollScoreText.textContent = this.#rollScore;\r\n    }\r\n}\r\n\r\n\n\n//# sourceURL=webpack://legion/./javascript/game_manager.js?");

/***/ }),

/***/ "./javascript/legion.js":
/*!******************************!*\
  !*** ./javascript/legion.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _game_manager_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./game_manager.js */ \"./javascript/game_manager.js\");\n// 'use-strict';\r\n\r\n\r\n\r\nconst soloButton = document.querySelector('#solo-btn');\r\n// const pandpButton = document.querySelector('#pandp-btn');\r\n// const aiButton = document.querySelector('#ai-btn');\r\nconst rulesModalButton = document.querySelector('#rules-btn');\r\nconst closeModalButton = document.querySelector('#close-modal-btn');\r\nconst rulesModal = document.querySelector('#rules-modal');\r\nconst rulesModalOverlay = document.querySelector('#overlay');\r\n\r\n\r\nclass App {\r\n\r\n    constructor() {    \r\n        \r\n        const isPassAndPlay = true;\r\n        const isVersesAI = true;\r\n\r\n        soloButton.addEventListener('click', this.#StartGame.bind(this, !isPassAndPlay, !isVersesAI));\r\n        // pandpButton.addEventListener('click', this.#StartGame.bind(this, isPassAndPlay, !isVersesAI));\r\n        // aiButton.addEventListener('click', this.#StartGame.bind(this, !isPassAndPlay, isVersesAI));\r\n\r\n        rulesModalButton.addEventListener('click', this.#OpenRulesModal);\r\n        closeModalButton.addEventListener('click', this.#CloseRulesModal);\r\n        rulesModalOverlay.addEventListener('click', this.#CloseRulesModal);\r\n\r\n        document.addEventListener('keydown', this.#EscapeModal.bind(this));\r\n    }\r\n\r\n    #PlayerCount() {\r\n\r\n        // implement get player count\r\n        return 2;\r\n    }\r\n\r\n    #StartGame(passAndPlay, versesAI) {\r\n\r\n        let playerCount = 1;\r\n        if (passAndPlay) playerCount = this.#PlayerCount();\r\n        if (versesAI) playerCount = 2;\r\n        this.GameManager = new _game_manager_js__WEBPACK_IMPORTED_MODULE_0__.GameManager(playerCount, versesAI);\r\n        this.#HideGameButtons();\r\n    }\r\n\r\n    #HideGameButtons() {\r\n        document.querySelector('.cont-score').classList.remove('invisible');\r\n        document.querySelector('.turn-btns').classList.remove('hidden');\r\n        document.querySelector('.mode-btns').classList.add('hidden');\r\n    }\r\n\r\n    #OpenRulesModal() {\r\n        rulesModal.classList.remove('hidden');\r\n        rulesModalOverlay.classList.remove('hidden');\r\n    }\r\n\r\n    #EscapeModal(event){\r\n        if (event.key === 'Escape' && !rulesModal.classList.contains('hidden'))\r\n            {\r\n                this.#CloseRulesModal(); \r\n            }\r\n    }\r\n\r\n    #CloseRulesModal(){\r\n        rulesModal.classList.add('hidden');\r\n        rulesModalOverlay.classList.add('hidden');\r\n    }\r\n\r\n}\r\n\r\nconst app = new App();\r\n\n\n//# sourceURL=webpack://legion/./javascript/legion.js?");

/***/ }),

/***/ "./javascript/player.js":
/*!******************************!*\
  !*** ./javascript/player.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   Player: () => (/* binding */ Player)\n/* harmony export */ });\n\r\nclass Player {\r\n\r\n    #playerID;\r\n    #totalScore = 0;\r\n\r\n    constructor(playerID) {\r\n        this.#playerID = playerID;\r\n    }\r\n\r\n    GetPlayerID(){\r\n        return this.#playerID;\r\n    }\r\n\r\n    GetTotalScore(){\r\n        return this.#totalScore;\r\n    }\r\n\r\n    SetTotalToZero(){\r\n        this.#totalScore = 0;\r\n    }\r\n\r\n    SetTotalScore(score){\r\n        this.#totalScore += score;\r\n    }\r\n}\r\n\r\n\n\n//# sourceURL=webpack://legion/./javascript/player.js?");

/***/ }),

/***/ "./javascript/score_checker.js":
/*!*************************************!*\
  !*** ./javascript/score_checker.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   ScoreChecker: () => (/* binding */ ScoreChecker)\n/* harmony export */ });\n/* harmony import */ var _support_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./support.js */ \"./javascript/support.js\");\n\r\n\r\nclass ScoreChecker {\r\n\r\n    #combinations;\r\n\r\n    CheckScore(currentRoll){\r\n\r\n        this.#combinations = this.CheckCombinations(currentRoll);\r\n        const scoring = this.#CreateScoringArray(this.#combinations, currentRoll);\r\n        const rollScore = this.#CalculateScoreFromCombinations(currentRoll);\r\n        const rollMessage = this.#CreateScoreMessage(this.#combinations, currentRoll);\r\n\r\n        return { scoring: scoring, combinations: this.#combinations, rollScore: rollScore, rollMessage: rollMessage }\r\n    }\r\n\r\n    CheckCombinations(diceArray){\r\n\r\n        const counts = this.#CountValues(diceArray);\r\n\r\n        const ThreePairs = function(counts){\r\n            let pairsCount = 0\r\n            Object.values(counts).forEach(function(count){\r\n                pairsCount += Math.trunc(count/2);\r\n            });\r\n            return pairsCount === 3;\r\n        }\r\n\r\n        const combinations = {\r\n            'sixOfAKind': diceArray.length === 6 && diceArray.every(value => value === diceArray[0]),\r\n            'oneOfEach': diceArray.length === 6 && Object.values(counts).every(value => value === 1),\r\n            'threePairs': ThreePairs(counts),\r\n            'threeMs': this.ThreeMs(diceArray),\r\n            'threeDs': this.ThreeDs(diceArray),\r\n            'threeCs': this.ThreeCs(diceArray),\r\n            'threeLs': this.ThreeLs(diceArray),\r\n            'fourVs': diceArray.filter(value => value === _support_js__WEBPACK_IMPORTED_MODULE_0__.dieFaces.v).length >= 4,\r\n            'xsOrVs': diceArray.includes(_support_js__WEBPACK_IMPORTED_MODULE_0__.dieFaces.v) || diceArray.includes(_support_js__WEBPACK_IMPORTED_MODULE_0__.dieFaces.x)\r\n        }\r\n        return combinations;\r\n    }\r\n\r\n    CalculateScoreIncompleteArray(diceArray){ // too much repitition - create a three of a kind method\r\n\r\n        let score = 0;\r\n\r\n        if (this.ThreeMs(diceArray)){ score = 1000; }\r\n        if (this.ThreeDs(diceArray)){ score += 500; }\r\n        if (this.ThreeCs(diceArray)){ score += 100; }\r\n        if (this.ThreeLs(diceArray)){ score += 50; }\r\n        score += diceArray.filter(value => value === _support_js__WEBPACK_IMPORTED_MODULE_0__.dieFaces.x).length * 10;\r\n        score += diceArray.filter(value => value === _support_js__WEBPACK_IMPORTED_MODULE_0__.dieFaces.v).length * 5;\r\n        return score;\r\n    }\r\n\r\n    #CreateScoringArray(combinations, currentRoll){\r\n\r\n        const counts = this.#CountValues(currentRoll);\r\n\r\n        let scoring = []\r\n\r\n        if(combinations.fourVs) { return scoring; }\r\n\r\n        if(combinations.oneOfEach || combinations.sixOfAKind || combinations.threePairs){\r\n            return currentRoll;\r\n        }\r\n        if (combinations.threeMs){ scoring.push(['m', 'm', 'm']); } // better way of adding to the array\r\n        if (combinations.threeLs){ scoring.push(['l', 'l', 'l']); }\r\n        if (combinations.threeCs){ scoring.push(['c', 'c', 'c']); }\r\n        if (combinations.threeDs){ scoring.push(['d', 'd', 'd']); }\r\n        if (combinations.xsOrVs){\r\n            for (const value of ['x', 'v']){\r\n                for (let count = 0; count < counts[value]; count++){\r\n                    scoring.push(value);\r\n                }\r\n            }\r\n        }\r\n        return scoring.flat();\r\n    }\r\n\r\n    #CreateScoreMessage(combinations, currentRoll){\r\n\r\n        let message = \"\";\r\n\r\n        if (combinations.fourVs) { \r\n            message = \"Four V's\";\r\n            return message;\r\n        }\r\n\r\n        if(combinations.oneOfEach){ message += \"One of each. \"; }\r\n        if(combinations.sixOfAKind){ message += \"Six of a kind. \"; }\r\n        if(combinations.threePairs){ message += \"Three pairs. \"; }\r\n        if(combinations.threeMs){ message += \"Three M's. \"; }\r\n        if(combinations.threeDs){ message += \"Three D's. \"; }\r\n        if(combinations.threeCs){ message += \"Three C's. \"; }\r\n        if(combinations.threeLs){ message += \"Three L's. \"; }\r\n        if(combinations.xsOrVs){\r\n            const counts = this.#CountValues(currentRoll);\r\n            if(counts.x > 0){\r\n                const xMessage = counts.x === 1 ? \"1 X. \" : `${counts.x} X's. `;\r\n                message += xMessage;\r\n            }\r\n            if(counts.v > 0){\r\n                const vMessage = counts.v === 1 ? \"1 V. \" : `${counts.v} V's. `;\r\n                message += vMessage;\r\n            }\r\n        }\r\n        return message;\r\n    }\r\n\r\n    #CalculateScoreFromCombinations(diceArray){\r\n\r\n        let rollScore = 0;\r\n\r\n        if(this.#combinations.fourVs) { return rollScore; }\r\n\r\n        if (diceArray.length = 6){\r\n            if (this.#combinations.sixOfAKind){\r\n                rollScore = 5000;\r\n                return rollScore;\r\n            }\r\n            if (this.#combinations.oneOfEach){\r\n                rollScore = 2000;\r\n                return rollScore;\r\n            }\r\n            if (this.#combinations.threePairs){\r\n                rollScore = 1000;\r\n                return rollScore;\r\n            }\r\n        }\r\n\r\n        if (this.#combinations.threeMs){\r\n            rollScore = 1000;\r\n        }\r\n        if (this.#combinations.threeDs){\r\n            rollScore += 500;\r\n        }\r\n        if (this.#combinations.threeCs){\r\n            rollScore += 100;   \r\n        }\r\n        if (this.#combinations.threeLs){\r\n            rollScore += 50;\r\n        }\r\n        if (this.#combinations.xsOrVs){\r\n            rollScore += diceArray.filter(value => value === _support_js__WEBPACK_IMPORTED_MODULE_0__.dieFaces.x).length * 10 + diceArray.filter(value => value === _support_js__WEBPACK_IMPORTED_MODULE_0__.dieFaces.v).length * 5;\r\n        }\r\n        return rollScore;\r\n    }\r\n\r\n    #CountValues(diceArray){\r\n        let counts = {\r\n            'v': 0,\r\n            'x': 0,\r\n            'l': 0,\r\n            'c': 0,\r\n            'd': 0,\r\n            'm': 0\r\n        };\r\n        diceArray.forEach(value => counts[value]++)\r\n        return counts;\r\n    }\r\n\r\n    ThreeMs(diceArray){\r\n        return diceArray.filter(value => value === _support_js__WEBPACK_IMPORTED_MODULE_0__.dieFaces.m).length >= 3\r\n    }\r\n\r\n    ThreeDs(diceArray){\r\n        return diceArray.filter(value => value === _support_js__WEBPACK_IMPORTED_MODULE_0__.dieFaces.d).length >= 3\r\n    }\r\n\r\n    ThreeCs(diceArray){\r\n        return diceArray.filter(value => value === _support_js__WEBPACK_IMPORTED_MODULE_0__.dieFaces.c).length >= 3\r\n    }\r\n\r\n    ThreeLs(diceArray){\r\n        return diceArray.filter(value => value === _support_js__WEBPACK_IMPORTED_MODULE_0__.dieFaces.l).length >= 3\r\n    }\r\n}\r\n\r\n \n\n//# sourceURL=webpack://legion/./javascript/score_checker.js?");

/***/ }),

/***/ "./javascript/support.js":
/*!*******************************!*\
  !*** ./javascript/support.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   dieFaces: () => (/* binding */ dieFaces)\n/* harmony export */ });\n\r\nconst dieFaces = {\r\n    v: 'v',\r\n    x: 'x',\r\n    l: 'l',\r\n    c: 'c',\r\n    d: 'd',\r\n    m: 'm'\r\n}\r\n\r\n\n\n//# sourceURL=webpack://legion/./javascript/support.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./javascript/legion.js");
/******/ 	
/******/ })()
;