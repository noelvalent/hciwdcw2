// store alphabet filter
const filterByAlpha = () => {
    const value = document.getElementById('store-alpha').value;
    if (value === '1'){
        location.href = `?`;
    } else{
        location.href = `?alpha=${value}`;
    }
}

const filterByCategory = () => {
    const value = document.getElementById('store-category').value;
    if (value === '---') {
        location.href = `?`;
    } else {
        location.href = `?category=${value}`;
    }
}