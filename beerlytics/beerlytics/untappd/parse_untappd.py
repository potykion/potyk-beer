import dataclasses


@dataclasses.dataclass
class UntappdBeer:
    title: str
    link: str
    style: str
    abv: float | None
    ibu: int | None
    rating: float | None
    rating_amount: int | None
    added: str | None

    @classmethod
    def parse(cls, raw):
        """
        >>> UntappdBeer.parse({
        ...   "title": "3 Fonteinen Oude Geuze",
        ...   "link": "https://untappd.com/b/brouwerij-3-fonteinen-3-fonteinen-oude-geuze/4009",
        ...   "style": "Lambic - Gueuze",
        ...   "abv": "6% ABV",
        ...   "ibu": "N/A IBU",
        ...   "rating": "(4.07)",
        ...   "ratingAmount": "74,444 Ratings",
        ...   "added": "Added 08/21/10"
        ... })
        UntappdBeer(title='3 Fonteinen Oude Geuze', link='https://untappd.com/b/brouwerij-3-fonteinen-3-fonteinen-oude-geuze/4009', style='Lambic - Gueuze', abv=6.0, ibu='', rating=4.07, rating_amount=74444, added='Added 08/21/10')

        """
        abv = raw.get('abv')
        if abv:
            abv = float(abv.replace('N/A', '0').replace("ABV", '').replace('%', '').strip())

        ibu = raw.get('ibu')
        if ibu:
            ibu = ibu.strip('IBU').replace('N/A', '0').strip()
            if ibu:
                ibu = int(ibu)

        rating = raw.get('rating')
        if rating:
            rating = rating.replace('N/A', '0').strip('(').strip(')')
            rating = float(rating)

        rating_amount = raw.get('ratingAmount')
        if rating_amount:
            rating_amount = rating_amount.strip('Ratings').strip()
            rating_amount = rating_amount.replace(',', '')
            rating_amount = int(rating_amount)

        return UntappdBeer(
            title=raw['title'],
            link=raw['link'],
            style=raw.get('style') or '',
            abv=abv or 0,
            ibu=ibu or 0,
            rating=rating or 0,
            rating_amount=rating_amount or 0,
            added=raw.get('added'),
        )