"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
document.addEventListener("DOMContentLoaded", () => {
    const myURL = 'http://127.0.0.1:8000/wordle/';
    function getCookieValue(name) {
        let cookieVal = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieVal = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
                ;
            }
            ;
        }
        ;
        return cookieVal;
    }
    ;
    const csrftoken = getCookieValue('csrftoken');
    function getEmptyRowIndex() {
        var _a;
        let Rows = document.querySelectorAll('.row');
        let arrayRows = Array.from(Rows);
        for (let i = 0; i < arrayRows.length; i++) {
            if (((_a = arrayRows[i].textContent) === null || _a === void 0 ? void 0 : _a.trim()) == "")
                return i;
        }
        ;
        return -1;
    }
    ;
    function getCurrentRow() {
        const n = getEmptyRowIndex();
        const rowId = 'row' + n;
        return document.getElementById(rowId);
    }
    ;
    let currentContainer = 0;
    let guess = "";
    let currentRow = getCurrentRow();
    let rowIndex = getEmptyRowIndex();
    document.addEventListener("keydown", (event) => __awaiter(void 0, void 0, void 0, function* () {
        const key = event.key;
        if (!currentRow)
            return;
        if (currentContainer < 0)
            currentContainer = 0;
        if (currentContainer > 5)
            currentContainer = 4;
        if (/^[a-zA-Z]$/.test(key) && currentContainer >= 0 && currentContainer <= 4) {
            currentRow.children[currentContainer].textContent = key.toUpperCase();
            guess = guess + key.toUpperCase();
            currentContainer++;
        }
        ;
        if (key === 'Backspace' && currentContainer <= 5 && currentContainer >= 1) {
            --currentContainer;
            currentRow.children[currentContainer].textContent = '';
            guess = guess.slice(0, currentContainer);
        }
        ;
        if (key === 'Enter' && currentContainer == 5) {
            if (getEmptyRowIndex() === -1) {
                window.location.reload();
                return;
            }
            ;
            try {
                const response = yield fetch(myURL, {
                    method: "POST",
                    headers: csrftoken ? { 'X-CSRFToken': csrftoken } : {},
                    body: JSON.stringify({ guess })
                });
                const data = yield response.json();
                // UPDATE GRID CSS 
                const rowData = data.guesses[rowIndex];
                for (let i = 0; i < 5; i++) {
                    const letterStatus = rowData[i].status;
                    if (letterStatus === 'correct') {
                        currentRow === null || currentRow === void 0 ? void 0 : currentRow.children[i].classList.add('correct');
                    }
                    else if (letterStatus === 'inside') {
                        currentRow === null || currentRow === void 0 ? void 0 : currentRow.children[i].classList.add('inside');
                    }
                    else if (letterStatus === 'wrong') {
                        currentRow === null || currentRow === void 0 ? void 0 : currentRow.children[i].classList.add('wrong');
                    }
                    ;
                }
                ;
                currentContainer = 0;
                guess = '';
                currentRow = getCurrentRow();
                rowIndex = getEmptyRowIndex();
            }
            catch (err) {
                alert(`Error ${err}`);
            }
            ;
        }
        ;
    }));
});
