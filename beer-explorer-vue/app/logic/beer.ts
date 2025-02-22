export interface Price {
    price: number;
    volume: string;

}

export interface VenuePrices {
    venue: string;
    prices: Price[];
}

export interface Beer {
    id?: string;

    brewery: string;
    name: string;
    rate: number;
    url: string;
    style: string;

    abv: number;
    ibu: number;

    venuePrices?: VenuePrices[];
}
