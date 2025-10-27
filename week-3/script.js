// window.addEventListener('DOMContentLoaded', () => {
//     const navIconMenu = document.querySelector('.nav_icon-menu');
//     const navIconClose = document.querySelector('.nav_icon-close');
//     const navMenu = document.querySelector('.nav_menu');

//     navIconMenu.addEventListener('click', () => {
//         navMenu.classList.add('is-open');
//     });

//     navIconClose.addEventListener('click', () => {
//         navMenu.classList.remove('is-open');
//     });
// });

const url_1 = 'https://cwpeng.github.io/test/assignment-3-1'
const url_2 = 'https://cwpeng.github.io/test/assignment-3-2'

const attractions = [];

async function fetchAttractionsData() {
    try {
        const response_1 = await fetch(url_1);
        const response_2 = await fetch(url_2);

        const data_url_1 = await response_1.json();
        const data_url_2 = await response_2.json();

        return [
            data_url_1.rows,
            data_url_2.rows
        ]
    }
    catch (error) {
        console.error('Error fetching attractions data:', error);
    }
}

async function mergeAttractionsData() {


}