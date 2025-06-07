document.addEventListener("DOMContentLoaded", async () => {
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
			if (arrayRows[i].textContent?.trim() == "") return i + 1;
		};
		return 1;

	};
	function getCurrentRow() {
		const rowId = 'row' + getEmptyRowIndex();
		return document.getElementById(rowId);

	};
	let currrentContainer = 0;
	let guess = "";
	let currentRow = getCurrentRow();

	document.addEventListener("keydown", async (event) => {
		const key = event.key;
		if (!currentRow) return;
		if (currrentContainer < 0) currrentContainer = 0;
		if (currrentContainer > 5) currrentContainer = 4;
		if (/^[a-zA-Z]$/.test(key) && currrentContainer >= 0 && currrentContainer <= 4) {
			currentRow.children[currrentContainer].textContent = key.toUpperCase();
			guess = guess + key.toUpperCase();
			currrentContainer++;
		};
		if (key === 'Backspace' && currrentContainer <= 5 && currrentContainer >= 1) {
			--currrentContainer;
			currentRow.children[currrentContainer].textContent = '';
			guess = guess.slice(0, currrentContainer);
		};
		if (key === 'Enter' && currrentContainer == 5) {
			try {
				await fetch(myURL, {
					method: "POST",
					headers: csrftoken ? { 'X-CSRFToken': csrftoken } : {},
					body: JSON.stringify({ guess })
				});
				currrentContainer = 0
				guess = ''
				currentRow = getCurrentRow()
			} catch (err) {
				alert(`Error ${err}`)
			};
		};
	});

});
