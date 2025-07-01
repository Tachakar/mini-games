const homeContent = document.getElementById("home-content");
if (homeContent) {
	setTimeout(() => { homeContent.classList.add("show") }, 200)
} else {
	alert("Something went wrong while loading main page.");
};
