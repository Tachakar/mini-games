const pageContent = document.getElementById("page-content");
if (pageContent) {
	setTimeout(() => { pageContent.classList.add("show") }, 200)
} else {
	alert("Something went wrong while loading main page.");
};
