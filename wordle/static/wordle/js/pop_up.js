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
    const pageContent = document.getElementById("page-content");
    if (word === null || !gameResult || !pageContent)
        return;
    // pageContent.style.filter = "blur(3px)";
    const popupOverlay = document.createElement('div');
    popupOverlay.id = "popup-overlay";
    document.body.appendChild(popupOverlay);
});
