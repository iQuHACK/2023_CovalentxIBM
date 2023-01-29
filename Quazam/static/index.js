// ================= DARK THEME ================

let matched = window.matchMedia("(prefers-color-scheme: dark)").matches;
const themeToggler = document.querySelector(".btn-theme-toggle");
const notificationSelector = document.querySelector(".notification-settings");

if (matched) {
	console.log("Currently in dark mode");
	document.body.classList.toggle("dark-mode");
	themeToggler.querySelector("span:nth-child(1)").classList.toggle("active");
	themeToggler.querySelector("span:nth-child(2)").classList.toggle("active");
} else {
	console.log("Currently in light mode.");
}

themeToggler.addEventListener("click", () => {
	document.body.classList.toggle("dark-mode");

	themeToggler.querySelector("span:nth-child(1)").classList.toggle("active");
	themeToggler.querySelector("span:nth-child(2)").classList.toggle("active");
});

// ================= MODAL ================
const openModalButton = document.getElementById("open-modal");
const modalContainer = document.getElementById("modal-container");
const closeModalButton = document.getElementById("close-modal")

openModalButton.addEventListener("click", () => {
    modalContainer.classList.add("active");
})

closeModalButton.addEventListener("click", () => {
    modalContainer.classList.remove("active");
})