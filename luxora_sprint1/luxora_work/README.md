# LUXORA - Premium E-Commerce Website

A modern, luxury-refined e-commerce platform built with vanilla HTML, CSS, and JavaScript. Perfect for beginners to understand multi-page web development and e-commerce functionality.

## 📁 Project Structure

```
luxora/
├── index.html          # Home page with hero section and category preview
├── products.html       # Products listing page with category filtering
├── cart.html          # Shopping cart with item management
├── styles.css         # Shared stylesheet for all pages
├── script.js          # Shared JavaScript (cart, products database)
├── products.js        # Products page specific functionality
├── cart.js            # Cart page specific functionality
└── README.md          # This file
```

## 🎨 Features

### Pages
- **Home Page** (index.html)
  - Elegant hero section with animated gradient
  - Category showcase with smooth hover effects
  - Quick navigation to product categories

- **Products Page** (products.html)
  - Browse all products or filter by category
  - Shoes, Electronics, Clothing, Books, Home Decor
  - 5 products per category (25 total products)
  - Add to cart functionality with notifications
  - Responsive product grid

- **Cart Page** (cart.html)
  - View all items in cart
  - Adjust quantities with +/- buttons
  - Remove items
  - Real-time order summary
  - Checkout simulation

### Functionality
- ✅ Add/remove items from cart
- ✅ Update product quantities
- ✅ LocalStorage persistence (cart data survives page refresh)
- ✅ Category filtering
- ✅ Real-time cart count in header
- ✅ Toast notifications for user actions
- ✅ Responsive design (mobile, tablet, desktop)

### Design
- 🎨 **Luxury Aesthetic**: Dark navy, gold accents, cream background
- ✨ **Smooth Animations**: Floating effects, fade transitions, hover states
- 💎 **Professional UI**: Sophisticated typography, spacing, shadows
- 📱 **Mobile Responsive**: Works seamlessly on all devices

## 🚀 Quick Start

1. **Download all files** to a single folder
2. **Open `index.html`** in your web browser
3. **Start shopping!** Navigate between pages using the menu

### File Setup
Ensure all files are in the same directory:
- HTML files (index.html, products.html, cart.html)
- CSS file (styles.css)
- JavaScript files (script.js, products.js, cart.js)

## 📝 File Descriptions

### HTML Files
- **index.html**: Home page with hero banner and category cards
- **products.html**: Product listing with filtering options
- **cart.html**: Shopping cart interface

### CSS
- **styles.css**: 
  - CSS variables for theme colors
  - Responsive grid layouts
  - Animations and transitions
  - Component styling (header, cards, buttons)

### JavaScript Files

#### script.js (Shared)
- Product database with 5 categories
- Cart management functions:
  - `loadCart()` - Load from localStorage
  - `saveCart()` - Save to localStorage
  - `addToCart(productId)` - Add item to cart
  - `removeFromCart(productId)` - Remove item
  - `updateQuantity(productId, quantity)` - Update quantity
  - `updateCartCount()` - Update header counter
- Notification system
- Page initialization

#### products.js (Products Page)
- `renderProducts(category)` - Display products
- `filterProducts(category)` - Filter by category
- URL parameter handling for category links

#### cart.js (Cart Page)
- `renderCart()` - Display cart items
- `updateQuantityAndRender()` - Update and re-render
- `removeAndRender()` - Remove and re-render
- `proceedToCheckout()` - Checkout simulation

## 💾 Data Persistence

The cart uses **localStorage** to save data:
```javascript
// Automatically saved
localStorage.setItem('luxora-cart', JSON.stringify(cart));

// Automatically loaded on page load
const saved = localStorage.getItem('luxora-cart');
```

Cart persists even after:
- ❌ Closing the tab/browser
- ❌ Refreshing the page
- ✅ Opening a new tab to the same domain

## 🎯 Product Categories

### Shoes (5 products)
- Leather Oxford
- Running Sneaker
- Loafer Casual
- Winter Boots
- Heeled Pump

### Electronics (5 products)
- Smart Watch
- Wireless Earbuds
- Tablet Pro
- Camera HD
- Laptop Stand

### Clothing (5 products)
- Silk Blouse
- Wool Sweater
- Tailored Blazer
- Denim Jeans
- Cashmere Scarf

### Books (5 products)
- The Midnight Library
- Atomic Habits
- Sapiens
- Project Hail Mary
- Educated

### Home Decor (5 products)
- Ceramic Vase
- Table Lamp
- Silk Cushion
- Wall Mirror
- Plant Pot

## 🎨 Color Scheme

```css
--primary-dark: #1a1a1a        /* Dark Navy */
--primary-gold: #d4af37        /* Luxury Gold */
--secondary-cream: #f5f3f0     /* Cream Background */
--text-dark: #2c2c2c           /* Dark Text */
--text-light: #666666          /* Light Gray */
--white: #ffffff               /* Pure White */
--accent-rose: #b8860b         /* Rose Gold */
```

## 📱 Responsive Breakpoints

- **Desktop**: Full layout (1400px max-width)
- **Tablet**: Adjusted grid (768px and below)
- **Mobile**: Single column where needed

## 🔧 Customization

### Add a New Product
Edit `script.js` and add to the products object:
```javascript
const products = {
    shoes: [
        // Add your product here
        { id: 26, name: 'Product Name', price: 9999, description: 'Description', emoji: '👟' }
    ]
};
```

### Change Colors
Edit CSS variables in `styles.css`:
```css
:root {
    --primary-gold: #your-color;
    --primary-dark: #your-color;
    /* etc */
}
```

### Add New Category
1. Add category to products object in `script.js`
2. Add category card in `index.html`
3. Update filter buttons in `products.html`

## ✨ Learning Outcomes

This project teaches:
- ✅ Multi-page website structure
- ✅ HTML semantic markup
- ✅ CSS Grid and Flexbox layouts
- ✅ CSS animations and transitions
- ✅ Vanilla JavaScript DOM manipulation
- ✅ LocalStorage for data persistence
- ✅ URL parameters handling
- ✅ Event handling and listeners
- ✅ State management
- ✅ Responsive design

## 🐛 Troubleshooting

### Cart not persisting
- Ensure browser allows localStorage
- Clear browser cache and reload
- Check browser console for errors

### Images not showing
- This project uses emoji instead of image files
- To use actual images, replace emoji with `<img>` tags

### Styling issues
- Verify all files are in the same directory
- Clear browser cache (Ctrl+Shift+Del)
- Check that styles.css is linked correctly

## 📚 Next Steps

To enhance this project:
1. **Add User Authentication** - Login/Registration system
2. **Add Payment Integration** - Stripe or Razorpay
3. **Backend Integration** - Node.js/Express API
4. **Database** - MongoDB or SQL database
5. **Search Functionality** - Search and filters
6. **Reviews & Ratings** - Customer feedback
7. **Admin Panel** - Product management
8. **Order History** - Track orders

## 📄 License

Free to use for learning and personal projects.

## 👨‍💻 Developer Notes

- All JavaScript is vanilla (no frameworks)
- No external dependencies required
- Works offline (except checkout)
- Fully responsive design
- Accessibility friendly

---

**Happy Shopping with LUXORA!** 🛍️✨
