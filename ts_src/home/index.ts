document.addEventListener('DOMContentLoaded', () => {
	try {
		const x = document.getElementById('home-content')
		if (!x) {
			throw new Error('Something went wrong.')
		}
		setTimeout(() => { x.classList.add('show') }, 200)
	}
	catch (err) {
		console.error(err)
	}
})
