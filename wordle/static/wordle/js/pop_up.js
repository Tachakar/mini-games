"use strict";
document.addEventListener("DOMContentLoaded", () => {
    function getLastWord() {
        const guesses = document.getElementsByClassName('row');
        for (let i = 0; i < guesses.length; i++) {
            const row = guesses[i];
            let rows = Array();
            for (let j = 0; j < 5; j++) {
                rows.push(row.children[j].textContent);
            }
            ;
            if (rows[i] == "     ") {
                return (rows[i - 1]);
            }
            ;
        }
        ;
        return null;
    }
    ;
    const word = getLastWord();
    if (word !== null) {
        // IN PROGRESS 
    }
    else {
        return;
    }
    ;
});
