const filterByCategory = () => {
    const value = document.getElementById('news-category').value;
    if (value === '-') {
        location.href = `?`;
    } else {
        location.href = `?category=${value}`;
    }
}