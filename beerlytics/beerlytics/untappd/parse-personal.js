// https://untappd.com/user/potykion/beers

const beers = [...document.querySelectorAll('.list-item')]
    .map(
        bi => {
            let imageTag = bi.querySelector('a.label > img')
            let imageUrl = imageTag.getAttribute('src')

            let beerDetails = bi.querySelector('.beer-details')
            let nameA = beerDetails.querySelector('.name a.track-click')
            let beer = nameA.innerText
            let beerUrl = nameA.href

            let breweryTag = beerDetails.querySelector('.brewery a')
            let breweryUrl = breweryTag.href
            let brewery = breweryTag.innerText

            let style = beerDetails.querySelector('.style').innerText

            let ratings = bi.querySelector('.ratings')
            let [myRating, globalRating] = [...ratings.querySelectorAll('.caps')]
                .map(caps => caps.getAttribute('data-rating'))
            // "3.59683" > 3.6
            myRating = parseFloat(parseFloat(myRating).toFixed(2))
            globalRating = parseFloat(parseFloat(globalRating).toFixed(2))

            let details = bi.querySelector('.details')
            let abv = details.querySelector('.abv').innerText
            // "4.5% ABV" > 4.5
            abv = parseFloat(abv.split('%')[0]);
            let ibu = details.querySelector('.ibu').innerText
            // "10 IBU" > 10, N/A IBU > 0
            ibu = ibu === 'N/A IBU' ? 0 : parseInt(ibu.split(' ')[0])

            return {
                imageUrl,
                beer,
                beerUrl,
                brewery,
                breweryUrl,
                style,
                myRating,
                globalRating,
                abv,
                ibu
            }
        }
    )

console.log(beers)