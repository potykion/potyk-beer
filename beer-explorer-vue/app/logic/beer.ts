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
    img?: string;

    tried?: boolean;
}


export function parseVolumeToL(vol: string): number {
    if (vol.toLowerCase() === "hot mug") return 0.25;

    vol = vol.split(" ")[0]!.toLowerCase();
    if (vol.endsWith("ml")) {
        const ml = parseFloat(vol.slice(0, vol.length - 2))
        return ml / 1000;
    } else {
        const l = parseFloat(vol.slice(0, vol.length - 1))
        return l
    }
}

export function compPricePerL(price: number, vol: string) {
    return Math.round(price / parseVolumeToL(vol));
}