export function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
export function displayValue(value) {
    return value == 0
        ? ""
        : value < 0
        ? "-$" + numberWithCommas((value * -1).toFixed(2))
        : "$" + numberWithCommas(value.toFixed(2));
}
