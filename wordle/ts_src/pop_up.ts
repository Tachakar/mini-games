document.addEventListener("DOMContentLoaded", () => {
	function getLastWord() {
		const guesses = document.getElementsByClassName('row');
		let allRows = Array();
		for (let i = 0; i < guesses.length; i++) {
			const row = guesses[i];
			let x = String();
			for (let j = 0; j < 5; j++) {
				x += (row.children[j].textContent);
			};
			allRows.push(x);
			if (x == "     ") {
				return (allRows[i - 1]);
			};
		};
		return null;
	};
	const word = getLastWord();
	if (word !== null) {
		const n = document.getElementsByTagName('body')[0];
		if (n !== null) {
			// to do
		};

	} else {
		return
	};

});
