let currentCategory = 'all';

// ===== RENDER PRODUCTS =====
function renderProducts(category = 'all', productList = null) {
    currentCategory = category;

    let allProducts = [];

    if (productList) {
        allProducts = productList;
    } else if (category === 'all') {
        for (let cat in products) {
            allProducts = allProducts.concat(products[cat]);
        }
    } else {
        allProducts = products[category] || [];
    }

    const container = document.getElementById('products-container');
    container.innerHTML = '';

    allProducts.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';

        const isInCart = cart.find(item => item.id === product.id);

        card.innerHTML = `
            <div class="product-image">${product.emoji}</div>
            <div class="product-info">
                <div class="product-name">${product.name}</div>
                <div class="product-description">${product.description}</div>
                <div class="product-footer">
                    <div class="product-price">₹${product.price.toLocaleString()}</div>
                    <button class="add-to-cart-btn ${isInCart ? 'added' : ''}" onclick="addToCart(${product.id})">
                        ${isInCart ? 'In Cart ✓' : 'Add to Cart'}
                    </button>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

// ===== SEARCH =====
function searchProducts() {
    const query = document.getElementById("searchInput").value.toLowerCase();

    let allProducts = [];
    for (let cat in products) {
        allProducts = allProducts.concat(products[cat]);
    }

    const filtered = allProducts.filter(p =>
        p.name.toLowerCase().includes(query)
    );

    renderProducts('all', filtered);
}

// ===== SORT =====
function sortProducts(type) {
    let allProducts = [];
    for (let cat in products) {
        allProducts = allProducts.concat(products[cat]);
    }

    if (type === 'low') {
        allProducts.sort((a, b) => a.price - b.price);
    } else {
        allProducts.sort((a, b) => b.price - a.price);
    }

    renderProducts('all', allProducts);
}

// ===== FILTER =====
function filterProducts(category) {
    renderProducts(category);
}

// ===== INIT =====
window.addEventListener('DOMContentLoaded', () => {
    renderProducts('all');
});