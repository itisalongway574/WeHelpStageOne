window.addEventListener('DOMContentLoaded', () => {
    const navIconMenu = document.querySelector('.nav_icon-menu');
    const navIconClose = document.querySelector('.nav_icon-close');
    const navMenu = document.querySelector('.nav_menu');

    navIconMenu.addEventListener('click', () => {
        navMenu.classList.add('is-open');
    });

    navIconClose.addEventListener('click', () => {
        navMenu.classList.remove('is-open');
    });
});