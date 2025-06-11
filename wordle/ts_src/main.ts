const myURL = 'http://127.0.0.1:8000/wordle/'
const WORD_LENGTH = 5;
const ANIMATION_DELAY_MS = 300;
document.addEventListener("DOMContentLoaded", () => {

	function getCookieValue(name: string) {
		let cookieVal = null;
		if (document.cookie && document.cookie !== '') {
			const cookies = document.cookie.split(';');
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				if (cookie.substring(0, name.length + 1) === (name + "=")) {
					cookieVal = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				};
			};
		};
		return cookieVal;
	};
	const csrftoken = getCookieValue('csrftoken');
	function getEmptyRowIndex() {
		let Rows = document.querySelectorAll('.row');
		let arrayRows = Array.from(Rows);
		for (let i = 0; i < arrayRows.length; i++) {
			if (arrayRows[i].textContent?.trim() == "") return i;
		};
		return -1;

	};
	function showPopup(winningWord: string, won: boolean, popupOverlay: HTMLElement, popupContent: HTMLElement) {
		if (won) {
			popupContent.textContent = "Good job, you've won!"
		} else {
			popupContent.textContent = `You've lost, try again. The word was: ${winningWord}`;
		}
		popupOverlay.classList.add('show');

	};
	function getCurrentRow() {
		const n = getEmptyRowIndex();
		const rowId = 'row' + n;
		return document.getElementById(rowId);

	};
	function applyLetterStatus(letterContainer: Element, letterStatus: string) {
		if (!letterContainer) return;
		letterContainer.classList.add('flip');
		if (letterStatus === 'correct') letterContainer.classList.add('correct');
		else if (letterStatus === 'inside') letterContainer.classList.add('inside');
		else if (letterStatus === 'wrong') letterContainer.classList.add('wrong');
	}
	async function processRowAnimations(guesses: { letter: string, status: string }[], row: HTMLElement) {
		const promises: Promise<void>[] = [];
		for (let i = 0; i < WORD_LENGTH; i++) {
			promises.push(
				new Promise((resolve) => {
					setTimeout(() => {
						applyLetterStatus(row.children[i], guesses[i].status);
						resolve();
					}, i * ANIMATION_DELAY_MS)
				})
			)
		};
		await Promise.all(promises)
	};
	let currentContainer = 0;
	let guess = "";
	let currentRow = getCurrentRow();
	let rowIndex = getEmptyRowIndex();

	document.addEventListener("keydown", async (event) => {
		const key = event.key;
		if (!currentRow) return;
		if (currentContainer < 0) currentContainer = 0;
		if (currentContainer > WORD_LENGTH) currentContainer = 4;
		if (/^[a-zA-Z]$/.test(key) && currentContainer >= 0 && currentContainer <= 4) {
			currentRow.children[currentContainer].textContent = key.toUpperCase();
			guess = guess + key.toUpperCase();
			currentContainer++;
		};
		if (key === 'Backspace' && currentContainer <= WORD_LENGTH && currentContainer >= 1) {
			--currentContainer;
			currentRow.children[currentContainer].textContent = '';
			guess = guess.slice(0, currentContainer);
		};
		if (key === 'Enter' && currentContainer == WORD_LENGTH) {
			try {
				const response = await fetch(myURL, {
					method: "POST",
					headers: csrftoken ? { 'X-CSRFToken': csrftoken } : {},
					body: JSON.stringify({ guess })
				})
				const data = await response.json();
				const guesses = data.guesses[rowIndex];
				await processRowAnimations(guesses, currentRow)

				if (data.game_over) {
					const popupOverlay = document.getElementById('popup-overlay');
					const popupConent = document.getElementById('popup-content');
					if (!popupConent || !popupOverlay) return;
					showPopup(data.winning_word, data.won, popupOverlay, popupConent);
					return;
				}
				currentContainer = 0;
				guess = '';
				currentRow = getCurrentRow();
				rowIndex = getEmptyRowIndex();
			} catch (err) {
				alert(`Error ${err}`)
				window.location.reload();
			};
		};
	});
});
