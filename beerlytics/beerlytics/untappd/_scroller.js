// [
//     "https://untappd.com/BakuninBrewery/beer",
//     "https://untappd.com/w/staatliches-hofbrauhaus-munchen/5566/beer",
//     "https://untappd.com/JawsBrew/beer",
//     "https://untappd.com/Plan_B_Brewery/beer",
//     "https://untappd.com/TrappistWestmalle/beer",
//     "https://untappd.com/Atmosphere_Brewery/beer"
// ]

const delay = milliseconds => new Promise(resolve => setTimeout(resolve, milliseconds));

async function scrollTillTheEnd() {
    while (true) {
        while (true) {
            let beforeScroll = window.scrollY
            window.scrollBy(0, 1000)
            if (window.scrollY === beforeScroll) {
                break
            }
        }

        const showMoreBtn = document.querySelector('.more-list-items')
        showMoreBtn.click()
        await delay(1000);
        if (showMoreBtn.style.display === 'none') {
            break
        }
        if (document.querySelectorAll('.beer-item').length > 300) {
            break
        }
    }

}

scrollTillTheEnd()