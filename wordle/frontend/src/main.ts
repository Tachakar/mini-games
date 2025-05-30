document.addEventListener("DOMContentLoaded", function() {
	const input = document.getElementById("guess-input") as HTMLInputElement | null;
	const currentRow = document.getElementById('current-row');

	if (!input || !currentRow) return;

	const letterContainers = document.querySelectorAll('.letter-container');

	input.addEventListener("input", function() {
		for (let i = 0; i < letterContainers.length; i++) {
			const letter = input.value[i];
			letterContainers[i].textContent = letter ? letter.toUpperCase() : "";
		}
	})
})
