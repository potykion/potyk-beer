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
    rating: number;
    url: string;
    style: string;

    venuePrices?: VenuePrices[];
}
