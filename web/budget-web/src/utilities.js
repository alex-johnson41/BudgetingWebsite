export function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
export function displayValue(value) {
    try {
        value = parseFloat(value);
        value = value.toFixed(2);
        return value == 0 ? "" : value < 0 ? "-$" + numberWithCommas(value * -1) : "$" + numberWithCommas(value);
    } catch (e) {
        return "";
    }
}
