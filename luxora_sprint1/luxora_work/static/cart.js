// ===== CART RENDERING =====
function renderCart() {
    if (cart.length === 0) {
        document.getElementById('cart-empty-state').style.display = 'block';
        document.getElementById('cart-content').style.display = 'none';
        return;
    }

    document.getElementById('cart-empty-state').style.display = 'none';
    document.getElementById('cart-content').style.display = 'grid';

    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = '';

    let subtotal = 0;
    cart.forEach(item => {
        subtotal += item.price * item.quantity;
        const itemTotal = item.price * item.quantity;
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        cartItem.innerHTML = `
            <div class="cart-item-image">${item.emoji}</div>
            <div class="cart-item-details">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">₹${item.price.toLocaleString()} each</div>
                <div style="color: var(--text-light); font-size: 0.9rem; margin-top: 0.3rem;">
                    Total: ₹${itemTotal.toLocaleString()}
                </div>
            </div>
            <div class="cart-item-controls">
                <button class="qty-button" onclick="updateQuantityAndRender(${item.id}, ${item.quantity - 1})">−</button>
                <input type="number" class="qty-input" value="${item.quantity}" onchange="updateQuantityAndRender(${item.id}, parseInt(this.value))">
                <button class="qty-button" onclick="updateQuantityAndRender(${item.id}, ${item.quantity + 1})">+</button>
                <button class="remove-btn" onclick="removeAndRender(${item.id})">Remove</button>
            </div>
        `;
        cartItems.appendChild(cartItem);
    });

    document.getElementById('subtotal').textContent = `₹${subtotal.toLocaleString()}`;
    document.getElementById('shipping').textContent = 'Free';
    document.getElementById('total').textContent = `₹${subtotal.toLocaleString()}`;
}

function updateQuantityAndRender(productId, quantity) {
    updateQuantity(productId, quantity);
    renderCart();
}

function removeAndRender(productId) {
    removeFromCart(productId);
    renderCart();
}

function proceedToCheckout() {
    if (cart.length === 0) {
        showNotification('Your cart is empty!');
        return;
    }
    
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    showNotification(`Processing checkout for ₹${total.toLocaleString()}!`);
    
    // Simulate checkout
    setTimeout(() => {
        showNotification('Order placed successfully!');
        cart = [];
        saveCart();
        renderCart();
    }, 2000);
}

// ===== INITIALIZE CART PAGE =====
window.addEventListener('DOMContentLoaded', () => {
    renderCart();
});
