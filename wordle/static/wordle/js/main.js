"use strict";
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById('guess-input') || null;
    if (!input)
        return;
    function getEmptyRow() {
        var _a;
        let Rows = document.querySelectorAll('.row');
        let arrayRows = Array.from(Rows);
        for (let i = 0; i < arrayRows.length; i++) {
            if (((_a = arrayRows[i].textContent) === null || _a === void 0 ? void 0 : _a.trim()) == "")
                return i + 1;
        }
        ;
        return 0;
    }
    ;
    const rowId = 'row' + getEmptyRow();
    const currentRow = document.getElementById(rowId);
    if (!currentRow)
        return;
    input.addEventListener("input", function () {
        for (let i = 0; i < 5; i++) {
            let letter = input.value[i];
            currentRow.children[i].textContent = letter ? letter : "";
        }
        ;
    });
});
