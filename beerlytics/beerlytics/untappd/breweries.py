import json

if __name__ == '__main__':
    with open('beer_db.json', encoding='utf-8') as f:
        breweries = json.load(f)
        breweries = {b["brewery"]['url'] for b in breweries}
        s= 'as'

    with open('new-breweries.txt', encoding='utf-8') as f:
        new_breweries = f.read().splitlines()
        new_breweries = {b for b in new_breweries if b not in breweries}
        print(new_breweries)
        with open('new-breweries.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_breweries))
        print('done')