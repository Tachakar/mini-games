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
document.addEventListener("DOMContentLoaded", () => __awaiter(void 0, void 0, void 0, function* () {
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
                return i + 1;
        }
        ;
        return 1;
    }
    ;
    function getCurrentRow() {
        const rowId = 'row' + getEmptyRowIndex();
        return document.getElementById(rowId);
    }
    ;
    let currrentContainer = 0;
    let guess = "";
    let currentRow = getCurrentRow();
    document.addEventListener("keydown", (event) => __awaiter(void 0, void 0, void 0, function* () {
        const key = event.key;
        if (!currentRow)
            return;
        if (currrentContainer < 0)
            currrentContainer = 0;
        if (currrentContainer > 5)
            currrentContainer = 4;
        if (/^[a-zA-Z]$/.test(key) && currrentContainer >= 0 && currrentContainer <= 4) {
            currentRow.children[currrentContainer].textContent = key.toUpperCase();
            guess = guess + key.toUpperCase();
            currrentContainer++;
        }
        ;
        if (key === 'Backspace' && currrentContainer <= 5 && currrentContainer >= 1) {
            --currrentContainer;
            currentRow.children[currrentContainer].textContent = '';
            guess = guess.slice(0, currrentContainer);
        }
        ;
        if (key === 'Enter' && currrentContainer == 5) {
            try {
                const response = yield fetch(myURL, {
                    method: 'POST',
                    headers: csrftoken ? {
                        "Content-Type": "applications/json",
                        "X-CSRFToken": csrftoken,
                    } : {},
                    body: JSON.stringify({ guess }),
                    credentials: "same-origin",
                });
                if (response.ok) {
                    guess = "";
                    currrentContainer = 0;
                    currentRow = getCurrentRow();
                }
                ;
            }
            catch (err) {
                alert(`Error ${err}`);
            }
            ;
            window.location.reload();
        }
        ;
    }));
}));
