// https://beruvyhodnoy.ru/stock/index.html

let countryOrType = '';

[...document.querySelectorAll("tr")].map(
    tr => {
        if (tr.querySelector('.header')) {
            countryOrType = tr.innerText;
            return [];
        } else if (tr.className === 'h') {
            return [...tr.querySelectorAll("td")].map(td => td.innerText).concat(countryOrType);
        } else {
            return [];
        }
    }
).filter(arr => arr.length)