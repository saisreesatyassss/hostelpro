// Add JavaScript to toggle the active class on the sidebar when the menu button is clicked

const menuButton = document.getElementById('menu-button');
const sidebar = document.querySelector('.sidebar');

menuButton.addEventListener('click', () => {
    sidebar.classList.toggle('active');
});
