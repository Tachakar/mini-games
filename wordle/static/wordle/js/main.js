"use strict";
document.addEventListener("DOMContentLoaded", function () {
    const URL = 'http://127.0.0.1:8000/wordle/';
    function getCsrfVal() {
        return;
    }
    ;
    function getEmptyRow() {
        var _a;
        let Rows = document.querySelectorAll('.row');
        let arrayRows = Array.from(Rows);
        for (let i = 0; i < arrayRows.length; i++) {
            if (((_a = arrayRows[i].textContent) === null || _a === void 0 ? void 0 : _a.trim()) == "")
                return i + 1;
        }
        ;
        return;
    }
    ;
    const rowId = 'row' + getEmptyRow();
    const currentRow = document.getElementById(rowId);
    if (!currentRow)
        return;
    let currrentContainer = 0;
    document.addEventListener("keydown", function (event) {
        const key = event.key;
        if (currrentContainer < 0) {
            currrentContainer = 0;
        }
        ;
        if (currrentContainer > 5) {
            currrentContainer = 4;
        }
        ;
        if (/^[a-zA-Z]$/.test(key) && currrentContainer >= 0) {
            currentRow.children[currrentContainer].textContent = key.toUpperCase();
            currrentContainer++;
        }
        ;
        if (key == 'Backspace' && currrentContainer <= 5) {
            --currrentContainer;
            currentRow.children[currrentContainer].textContent = '';
        }
        ;
        if (key == 'Enter' && currrentContainer == 5) {
            const response = fetch(URL, {
                method: "POST",
            });
        }
        ;
    });
});
