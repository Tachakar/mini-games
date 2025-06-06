"use strict";
document.addEventListener("DOMContentLoaded", () => {
    function getLastWord() {
        const guesses = document.getElementsByClassName('row');
        let allRows = Array();
        for (let i = 0; i < guesses.length; i++) {
            const row = guesses[i];
            let x = String();
            for (let j = 0; j < 5; j++) {
                x += (row.children[j].textContent);
            }
            ;
            allRows.push(x);
            if (x == "     ") {
                return (allRows[i - 1]);
            }
            ;
        }
        ;
        return null;
    }
    ;
    const word = getLastWord();
    const gameResult = document.getElementById('game-result');
    const popupOverlay = document.getElementById('popup-overlay');
    if (word == null || !gameResult || !popupOverlay)
        return;
    if (gameResult.dataset.won == 'true') {
        popupOverlay.classList.remove('hidden');
    }
    ;
});
