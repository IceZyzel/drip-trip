const categories = document.querySelectorAll('.category');

categories.forEach(category => {
    category.addEventListener('click', () => {
        categories.forEach(c => c.classList.remove('active'));
        category.classList.add('active');
    });
});


const filterCategories = document.querySelectorAll('.filter-category');

filterCategories.forEach(category => {
    const title = category.querySelector('.category-title');

    title.addEventListener('click', () => {
        title.classList.toggle('active');
    });
});

