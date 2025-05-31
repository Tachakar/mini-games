document.addEventListener("DOMContentLoaded", function() {

	const input = document.getElementById('guess-input') as HTMLInputElement || null;
	if (!input) return;

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



	input.addEventListener("input", function() {
		for (let i = 0; i < 5; i++) {
			let letter = input.value[i];
			currentRow.children[i].textContent = letter ? letter : "";
		};
	});
});
