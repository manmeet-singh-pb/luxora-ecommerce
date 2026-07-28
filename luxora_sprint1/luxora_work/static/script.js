// ===== FETCH DATA FROM PYTHON BACKEND =====
// Notice how the big list of products is gone! We start empty.
let products = {};
let cart = [];

async function fetchProducts() {
    try {
        // Relative path works no matter what host/port Flask runs on
        const response = await fetch('/api/products');
        const data = await response.json();
        products = data; // Save the data from Python
        
        console.log("Products successfully loaded from server!", products);
        
        // If we are on the products.html page, render them now that we have data
        if (typeof renderProducts === "function") {
            renderProducts('all');
        }
    } catch (error) {
        console.error("Error fetching products:", error);
        showNotification("Failed to connect to the Python server.");
    }
}

// ===== CART MANAGEMENT =====
function loadCart() {
    const saved = localStorage.getItem('luxora-cart');
    cart = saved ? JSON.parse(saved) : [];
    updateCartCount();
}

function saveCart() {
    localStorage.setItem('luxora-cart', JSON.stringify(cart));
    updateCartCount();
}

function addToCart(productId) {
    const product = findProduct(productId);
    if (!product) return;

    const existingItem = cart.find(item => item.id === productId);
    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({ ...product, quantity: 1 });
    }

    saveCart();
    showNotification(`${product.name} added to cart!`);
    updateProductButton(productId);
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    saveCart();
}

function updateQuantity(productId, quantity) {
    if (quantity <= 0 || isNaN(quantity)) {
        removeFromCart(productId);
        return;
    }

    const item = cart.find(item => item.id === productId);
    if (item) {
        item.quantity = quantity;
        saveCart();
    }
}

function updateCartCount() {
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);
    document.querySelectorAll('#cart-count').forEach(el => {
        el.textContent = count;
    });
}

function findProduct(productId) {
    for (let category in products) {
        const found = products[category].find(p => p.id === productId);
        if (found) return found;
    }
    return null;
}

// ===== NOTIFICATION =====
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

function updateProductButton(productId) {
    const btn = document.getElementById(`btn-${productId}`);
    if (btn) {
        btn.textContent = 'Added ✓';
        btn.classList.add('added');
        setTimeout(() => {
            btn.textContent = 'Add to Cart';
            btn.classList.remove('added');
        }, 1500);
    }
}

// ===== AUTH SYSTEM =====
function checkUser() {
    const user = JSON.parse(localStorage.getItem("luxora-user"));

    const loginLink = document.getElementById("login-link");
    const logoutLink = document.getElementById("logout-link");

    if (user) {
        if(loginLink) loginLink.style.display = "none";
        if(logoutLink) logoutLink.style.display = "inline-block";
    } else {
        if(loginLink) loginLink.style.display = "inline-block";
        if(logoutLink) logoutLink.style.display = "none";
    }
}

function logout() {
    localStorage.removeItem("luxora-user");
    alert("Logged out!");
    window.location.href = "index.html";
}

// ===== INITIALIZE =====
window.addEventListener('DOMContentLoaded', () => {
    fetchProducts(); // <-- This line tells your site to ask Python for the data!
    loadCart();
    checkUser(); 

    // Handle Active Navigation Links
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('nav a').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
});
/* ===== STICKY NAVBAR SCROLL EFFECT ===== */

const header = document.querySelector("header");

function handleScrollEffect() {
    if (!header) return;

    if (window.scrollY > 10) {
        header.classList.add("scrolled");
    } else {
        header.classList.remove("scrolled");
    }
}

// Listen for scroll events
window.addEventListener("scroll", handleScrollEffect, { passive: true });

// Run once when page loads
handleScrollEffect();