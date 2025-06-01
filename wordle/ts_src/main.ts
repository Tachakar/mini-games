document.addEventListener("DOMContentLoaded", function() {

	function getEmptyRow() {
		let Rows = document.querySelectorAll('.row');
		let arrayRows = Array.from(Rows);
		for (let i = 0; i < arrayRows.length; i++) {
			if (arrayRows[i].textContent?.trim() == "") return i + 1;
		};
		return;

	};
	const rowId = 'row' + getEmptyRow();
	const currentRow = document.getElementById(rowId);
	if (!currentRow) return;
	let currrentContainer = 0;

	document.addEventListener("keydown", function(event) {
		console.log(currrentContainer);
		const key = event.key;
		if (currrentContainer < 0) {
			currrentContainer = 0;
		};
		if (currrentContainer > 5) {
			currrentContainer = 4;
		};
		if (/^[a-zA-Z]$/.test(key) && currrentContainer >= 0) {
			currentRow.children[currrentContainer].textContent = key.toUpperCase();
			currrentContainer++;
		};
		if (key == 'Backspace' && currrentContainer <= 5) {
			--currrentContainer;
			currentRow.children[currrentContainer].textContent = '';
		};
	});
});
