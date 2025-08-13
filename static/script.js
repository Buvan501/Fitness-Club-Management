document.addEventListener('DOMContentLoaded', () => {
    // Enable tooltips
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
        new bootstrap.Tooltip(el);
    });

    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            alert('Thank you for your message! We will get back to you shortly.');
            contactForm.reset();
        });
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        // Minimal validation feedback
        loginForm.addEventListener('submit', function(e) {
            const required = loginForm.querySelectorAll('[required]');
            let isValid = true;
            required.forEach(f => {
                if (!f.value.trim()) {
                    f.classList.add('is-invalid');
                    isValid = false;
                } else {
                    f.classList.remove('is-invalid');
                }
            });
            if (!isValid) {
                e.preventDefault();
            }
        });

        // Show/hide password
        const toggle = document.getElementById('toggle-password');
        const password = document.getElementById('password');
        if (toggle && password) {
            toggle.addEventListener('click', () => {
                const showing = password.getAttribute('type') === 'text';
                password.setAttribute('type', showing ? 'password' : 'text');
                toggle.setAttribute('aria-pressed', String(!showing));
                const icon = toggle.querySelector('i');
                if (icon) {
                    icon.classList.toggle('bi-eye');
                    icon.classList.toggle('bi-eye-slash');
                }
            });
        }
    }
});

// No custom JS needed for Bootstrap navbar; Bootstrap handles toggling