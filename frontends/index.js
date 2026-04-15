// Signup Form Submission Handler
document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');
    const signupButton = document.getElementById('signupButton');
    const buttonText = document.getElementById('buttonText');
    const buttonIcon = document.getElementById('buttonIcon');
    const loader = document.getElementById('loader');
    const formError = document.getElementById('formError');
    const passwordInput = document.getElementById('password');

    if (signupForm && signupButton) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Validate password
            if (passwordInput) {
                const password = passwordInput.value;
                const minLength = password.length >= 8;
                // Check if there is at least one character that is not a letter or digit (i.e., a special character)
                // We'll also treat space as NOT a special character just to be strict
                const hasSpecialChar = /[^A-Za-z0-9\s]/.test(password);

                if (!minLength || !hasSpecialChar) {
                    if (formError) {
                        formError.textContent = 'Password must be at least 8 characters with 1 special character.';
                        formError.classList.remove('hidden');
                    }
                    return; // Stop form submission
                }
            }

            // Hide error if validation passes
            if (formError) {
                formError.classList.add('hidden');
            }

            // Premium Loading State
            signupButton.disabled = true;
            if (buttonText) buttonText.textContent = 'Creating Account...';
            if (buttonIcon) buttonIcon.classList.add('hidden');
            if (loader) loader.classList.remove('hidden');
            signupButton.classList.add('opacity-90', 'cursor-not-allowed');

            // Simulate processing delay for "WOW" effect
            setTimeout(() => {
                window.location.href = signupForm.getAttribute('action');
            }, 1500);
        });
    }
});
