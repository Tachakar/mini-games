const gameData = document.getElementById('game-data')?.dataset;
let gameId: string
if (gameData !== undefined && gameData.gameId !== undefined) {

	gameId = gameData.gameId
} else {
	gameId = "error"
}
const API_URL = `wordle/game/${gameId}/check/`
const WORD_LENGTH = 5;
const ANIMATION_DELAY_MS = 300;
function getCookieValue(name: string) {
	let cookieVal = "";
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + "=")) {
				cookieVal = decodeURIComponent(cookie.substring(name.length + 1));
				return cookieVal;
			};
		};
	};
	return null
};
function getEmptyRowIndex() {
	const Rows = document.querySelectorAll('.row');
	const arrayRows = Array.from(Rows);
	for (let i = 0; i < arrayRows.length; i++) {
		if (arrayRows[i].textContent?.trim() == "") return i;
	};
	return -1

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
function applyLetterStatus(letter: Element, letterData: { letter: string, status: string }) {
	const letterStatus = letterData.status;
	if (!letter) return;
	letter.classList.add('flip');
	letter.children[0].classList.add('after');
	if (letterStatus === 'correct') letter.classList.add('correct');
	else if (letterStatus === 'inside') letter.classList.add('inside');
	else if (letterStatus === 'wrong') letter.classList.add('wrong');
}
async function processRowAnimations(guessesData: { letter: string, status: string }[], row: HTMLElement) {
	const promises: Promise<void>[] = [];
	for (let i = 0; i < WORD_LENGTH; i++) {
		const letter = row.children[i];
		promises.push(
			new Promise((resolve) => {
				setTimeout(() => {
					applyLetterStatus(letter, guessesData[i]);
					resolve();
				}, i * ANIMATION_DELAY_MS)
			})
		)
	};
	await Promise.all(promises)
};
const csrftoken = getCookieValue('csrftoken');
let containerIndex = 0;
let guess = "";
let row = getCurrentRow();
let rowIndex = getEmptyRowIndex();


document.addEventListener("keydown", async (event) => {
	const key = event.key;
	if (!row) return;
	if (containerIndex < 0) containerIndex = 0;
	if (containerIndex > WORD_LENGTH) containerIndex = WORD_LENGTH;
	if (/^[a-zA-Z]$/.test(key) && containerIndex >= 0 && containerIndex <= (WORD_LENGTH - 1)) {
		const letterContainer = row.children[containerIndex].children[0];
		letterContainer.textContent = key.toUpperCase();
		guess = guess + key.toUpperCase();
		containerIndex++;
	};
	if (key === 'Backspace' && containerIndex <= WORD_LENGTH && containerIndex >= 1) {
		containerIndex--;
		const letterContainer = row.children[containerIndex].children[0];
		letterContainer.textContent = " ";
		guess = guess.slice(0, -1);
	};
	if (key === 'Enter' && containerIndex == WORD_LENGTH) {
		try {
			const response = await fetch('check/', {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": csrftoken || "",
				},
				body: JSON.stringify({ guess }),
			})

			if (!response.ok) {
				throw new Error(`HTTP error, status: ${response.status}`)
			}
			const data = await response.json();
			if (!data.guesses || !data.guesses[rowIndex]) {
				throw new Error('Invalid response format')
			}
			const guesses = data.guesses[rowIndex];
			await processRowAnimations(guesses, row)

			if (data.game_over) {
				const popupOverlay = document.getElementById('popup-overlay');
				const popupConent = document.getElementById('popup-content');
				if (!popupConent || !popupOverlay) return;
				showPopup(data.winning_word, data.won, popupOverlay, popupConent);
				return;
			}
			containerIndex = 0;
			guess = '';
			row = getCurrentRow();
			rowIndex = getEmptyRowIndex();
		} catch (err) {
			alert(`Error: ${err}`)
			window.location.reload();
		};
	};
});
