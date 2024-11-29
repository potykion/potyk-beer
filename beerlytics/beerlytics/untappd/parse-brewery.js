// https://untappd.com/Brouwerij3Fonteinen/beer


const brewery = (() => {
    let breweryTag = document.querySelector('.b_info .name');

    return {
        title: breweryTag.querySelector('h1').innerText,
        location: breweryTag.querySelector('.brewery').innerText,
        url: location.href
    }
})();

const beers = [...document.querySelectorAll('.beer-item')]
    .map(
        beerItem => {
            let title = beerItem.querySelector('.beer-details').querySelector('.name').innerText
            let link = beerItem.querySelector('.beer-details').querySelector('.name > a').href

            let style = beerItem.querySelector('.beer-details').querySelector('.style').innerText

            let abv = beerItem.querySelector('.details').querySelector('.abv').innerText.trim();
            let ibu = beerItem.querySelector('.details').querySelector('.ibu').innerText.trim();
            let rating = beerItem.querySelector('.details').querySelector('.num').innerText.trim();
            let ratingAmount = beerItem.querySelector('.details').querySelector('.raters').innerText.trim();
            let added = beerItem.querySelector('.details').querySelector('.date').innerText.trim();

            // "6.7% ABV" > 6.7
            try {
                abv = abv.includes('N/A') ? 0 : parseFloat(abv.split('%')[0])

            } catch (e) {
                console.error(title, `abv = ${abv}`)
            }
            // "Added 10/20/10" > "10/20/10"
            try {
                added = added.slice(6)
            } catch (e) {
                console.error(title, `added = ${added}`)
            }
            // "24 IBU" > 24
            ibu = ibu.includes('N/A') ? 0 : parseInt(ibu.split(' '))
            // "(3.77)" > 3.77
            try {
                rating = rating.includes('N/A') ? 0 : parseFloat(rating.slice(1, -1))

            } catch (e) {
                console.error(title, `rating = ${rating}`)

            }
            // "168,259 Ratings" > 168259
            ratingAmount = parseInt(ratingAmount.split(' ')[0].replace(',', ''))

            let [mainStyle, subStyle] = ['', ''];
            if (style.includes(' - ')) {
                [mainStyle, subStyle] = style.split(' - ')
            } else {
                mainStyle = style
            }

            let breweryLink = location.href;

            return {
                title, link, style, abv, ibu, rating, ratingAmount, added,
                mainStyle,
                subStyle, breweryLink,
            }
        }
    )

console.log({brewery, beers})
