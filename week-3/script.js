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

const url_1 = 'https://cwpeng.github.io/test/assignment-3-1'
const url_2 = 'https://cwpeng.github.io/test/assignment-3-2'


async function fetchAttractionsData() {
    try {
        const response_1 = await fetch(url_1);
        const response_2 = await fetch(url_2);

        const data_url_1 = await response_1.json();
        const data_url_2 = await response_2.json();

        return {
            attractions_info: data_url_1.rows,
            attractions_pics: data_url_2.rows
        }
    }
    catch (error) {
        console.error('Error fetching attractions data:', error);
    }
}

function mergeAttractionsData(attractions_info, attractions_pics) {

    // map出attractions_pics的serial和pics
    const attractions_pics_map = new Map();
    attractions_pics.forEach(pics => {
        attractions_pics_map.set(pics.serial, pics.pics);
    });

    const mergedAttractions = attractions_info.map(info => {
        const serial = info.serial;
        // 找出對應的serial
        const matchedSerial = attractions_pics_map.get(serial);
        if (matchedSerial) {
            const rawPics = matchedSerial;
            const splitBase = '.jpg';
            const cleanPics = rawPics.split(splitBase);
            const picsUrl = 'https://www.travel.taipei/' + cleanPics[0] + '.jpg';
            // console.log(picsUrl);

            return {
                name: info.sname,
                pics: picsUrl
            }
        } else {
            return {
                name: info.sname,
                pics: ''
            }
        }
    })
    console.log(mergedAttractions);
    return mergedAttractions;
}

function renderDOM(mergedAttractions) {
    const first3attractions = mergedAttractions.slice(0, 3);
    // console.log(first3attractions);
    const otherAttractions = mergedAttractions.splice(3);
    // console.log(otherAttractions);

    const promotionsContainer = document.querySelector('.promotions_container');
    const mainContainer = document.querySelector('.main_container');

    // 渲染promotions
    first3attractions.forEach((atttraction, index) => {
        const promotionDiv = document.createElement('div');
        promotionDiv.classList.add('promotion');
        promotionDiv.classList.add('promotion-' + (index + 1));

        const promotionImg = document.createElement('img');
        promotionImg.src = atttraction.pics;
        promotionImg.classList.add('promotion-img');
        promotionImg.alt = atttraction.name;
        promotionDiv.appendChild(promotionImg);

        const promotionText = document.createElement('p');
        promotionText.textContent = atttraction.name;
        promotionDiv.appendChild(promotionText);
        promotionsContainer.appendChild(promotionDiv);
    })

    // 每10個attractions渲染一個cards_container
    // 先判斷otherAttractions的長度是否大於10
    const cardContainer = document.createElement('section');
    cardContainer.classList.add('cards_container');

    otherAttractions.forEach((atttraction, index) => {

        const cardDiv = document.createElement('div');
        cardDiv.classList.add('card');
        cardDiv.classList.add('card-' + (index + 1));

        const cardImg = document.createElement('img');
        cardImg.src = atttraction.pics;
        cardImg.classList.add('card-img');
        cardImg.alt = atttraction.name;
        cardDiv.appendChild(cardImg);

        const cardStar = document.createElement('img');
        cardStar.src = 'assets/star.svg';
        cardStar.classList.add('card-star');
        cardStar.alt = 'star';
        cardDiv.appendChild(cardStar);

        const cardTextBlock = document.createElement('div');
        cardTextBlock.classList.add('card_text-block');
        const cardText = document.createElement('p');
        cardText.textContent = atttraction.name;
        cardTextBlock.appendChild(cardText);
        cardDiv.appendChild(cardTextBlock);
        cardContainer.appendChild(cardDiv);
        mainContainer.appendChild(cardContainer);
    })
}


fetchAttractionsData().
    then(data => {
        return mergeAttractionsData(data.attractions_info, data.attractions_pics);
    })
    .then(mergedAttractions => {
        renderDOM(mergedAttractions);
    });