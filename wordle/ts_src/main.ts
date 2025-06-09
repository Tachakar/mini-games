document.addEventListener("DOMContentLoaded", () => {
	const myURL = 'http://127.0.0.1:8000/wordle/'

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
	function getCurrentRow() {
		const n = getEmptyRowIndex();
		const rowId = 'row' + n;
		return document.getElementById(rowId);

	};
	let currentContainer = 0;
	let guess = "";
	let currentRow = getCurrentRow();
	let rowIndex = getEmptyRowIndex();

	document.addEventListener("keydown", async (event) => {
		const key = event.key;
		if (!currentRow) return;
		if (currentContainer < 0) currentContainer = 0;
		if (currentContainer > 5) currentContainer = 4;
		if (/^[a-zA-Z]$/.test(key) && currentContainer >= 0 && currentContainer <= 4) {
			currentRow.children[currentContainer].textContent = key.toUpperCase();
			guess = guess + key.toUpperCase();
			currentContainer++;
		};
		if (key === 'Backspace' && currentContainer <= 5 && currentContainer >= 1) {
			--currentContainer;
			currentRow.children[currentContainer].textContent = '';
			guess = guess.slice(0, currentContainer);
		};
		if (key === 'Enter' && currentContainer == 5) {
			try {
				const response = await fetch(myURL, {
					method: "POST",
					headers: csrftoken ? { 'X-CSRFToken': csrftoken } : {},
					body: JSON.stringify({ guess })
				})
				const data = await response.json();
				// UPDATE GRID STYLE 
				const rowData = data.guesses[rowIndex];
				for (let i = 0; i < 5; i++) {
					const letterStatus = rowData[i].status;
					if (letterStatus === 'correct') {
						currentRow?.children[i].classList.add('correct')
					} else if (letterStatus === 'inside') {
						currentRow?.children[i].classList.add('inside')
					} else if (letterStatus === 'wrong') {
						currentRow?.children[i].classList.add('wrong')
					};
				}
				// CHECH IF GAME IS OVER
				if (data.game_over) {
					const popupOverlay = document.getElementById('popup-overlay');
					const popupContent = document.getElementById('popup-content');
					if (!popupContent || !popupOverlay) return;
					if (data.won) {
						popupContent.textContent = "Good job, you've won!"
					} else {

						popupContent.textContent = "You've lost, please try again."
					}
					popupOverlay.classList.remove('hidden')
					event.currentTarget?.removeEventListener("keydown")
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
