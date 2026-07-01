/* ==========================================================================
   ShopSphere - Premium Interactions JavaScript
   Includes: Password toggles, scroll-to-top buttons, quantity increments,
             wishlist interactions (localStorage based), and loading overlays.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    // ---------- Show / Hide Password ----------
    var toggleButtons = document.querySelectorAll('.password-toggle-btn');

    toggleButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            var input = btn.parentElement.querySelector('input');

            if (input.type === 'password') {
                input.type = 'text';
                btn.textContent = 'Hide';
            } else {
                input.type = 'password';
                btn.textContent = 'Show';
            }
        });
    });


    // ---------- Scroll To Top Button ----------
    var scrollBtn = document.getElementById('scrollTopBtn');

    if (scrollBtn) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 300) {
                scrollBtn.classList.add('visible');
            } else {
                scrollBtn.classList.remove('visible');
            }
        });

        scrollBtn.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }


    // ---------- Quantity Increase / Decrease ----------
    var qtyMinusBtns = document.querySelectorAll('.qty-minus');
    var qtyPlusBtns = document.querySelectorAll('.qty-plus');

    qtyMinusBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            var input = btn.parentElement.querySelector('.qty-input');
            var value = parseInt(input.value);

            if (value > 1) {
                input.value = value - 1;
            }
        });
    });

    qtyPlusBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            var input = btn.parentElement.querySelector('.qty-input');
            var value = parseInt(input.value);
            var max = parseInt(input.getAttribute('max')) || 99;

            if (value < max) {
                input.value = value + 1;
            }
        });
    });


    // ---------- Password Strength Indicator (Register Page) ----------
    var passwordInput = document.getElementById('id_password1');
    var strengthBar = document.getElementById('passwordStrengthBar');

    if (passwordInput && strengthBar) {
        passwordInput.addEventListener('input', function () {
            var password = passwordInput.value;
            var strength = 0;

            if (password.length >= 6) {
                strength = strength + 1;
            }
            if (password.length >= 10) {
                strength = strength + 1;
            }
            if (/[A-Z]/.test(password) && /[0-9]/.test(password)) {
                strength = strength + 1;
            }

            strengthBar.className = 'password-strength-bar';

            if (strength === 1) {
                strengthBar.classList.add('strength-weak');
            } else if (strength === 2) {
                strengthBar.classList.add('strength-medium');
            } else if (strength >= 3) {
                strengthBar.classList.add('strength-strong');
            }
        });
    }


    // ---------- Wishlist (saved in browser localStorage) ----------
    var wishlistBtns = document.querySelectorAll('.wishlist-btn');
    var wishlist = JSON.parse(localStorage.getItem('shopsphere_wishlist') || '[]');

    wishlistBtns.forEach(function (btn) {
        var productId = btn.getAttribute('data-product-id');

        // Mark as active if already in wishlist
        if (wishlist.indexOf(productId) !== -1) {
            btn.classList.add('active');
            btn.innerHTML = '<i class="bi bi-heart-fill"></i>';
        }

        btn.addEventListener('click', function (e) {
            e.preventDefault();
            var index = wishlist.indexOf(productId);

            if (index === -1) {
                // Add to wishlist
                wishlist.push(productId);
                btn.classList.add('active');
                btn.innerHTML = '<i class="bi bi-heart-fill"></i>';
            } else {
                // Remove from wishlist
                wishlist.splice(index, 1);
                btn.classList.remove('active');
                btn.innerHTML = '<i class="bi bi-heart"></i>';
            }

            localStorage.setItem('shopsphere_wishlist', JSON.stringify(wishlist));
        });
    });


    // ---------- Simple Loading Spinner on Form Submit ----------
    var forms = document.querySelectorAll('form.show-loading');
    var loadingOverlay = document.getElementById('loadingOverlay');

    forms.forEach(function (form) {
        form.addEventListener('submit', function () {
            if (loadingOverlay) {
                loadingOverlay.classList.add('show');
            }
        });
    });


    // ---------- Newsletter Form (frontend only demo) ----------
    var newsletterForm = document.getElementById('newsletterForm');

    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function (e) {
            e.preventDefault();
            alert('Thank you for subscribing to the ShopSphere newsletter!');
            newsletterForm.reset();
        });
    }

});
