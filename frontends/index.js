// Signup Form Submission Handler
document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');
    const signupButton = document.getElementById('signupButton');
    const buttonText = document.getElementById('buttonText');
    const buttonIcon = document.getElementById('buttonIcon');
    const loader = document.getElementById('loader');
    const formError = document.getElementById('formError');
    const passwordInput = document.getElementById('password');
    const passwordHint = document.getElementById('passwordHint');
    const passwordHintIcon = document.getElementById('passwordHintIcon');
    const passwordHintText = document.getElementById('passwordHintText');

    // Real-time validation clear
    if (passwordInput && passwordHint) {
        passwordInput.addEventListener('input', () => {
             passwordHint.classList.remove('text-red-500', 'dark:text-red-400', 'animate-pulse');
             passwordHint.classList.add('text-slate-500', 'dark:text-slate-400');
             if (passwordHintIcon) passwordHintIcon.classList.add('hidden');
             if (passwordHintText) passwordHintText.textContent = 'Must be at least 8 characters with 1 special character.';
             passwordInput.classList.remove('ring-red-500', 'dark:ring-red-400', 'focus:ring-red-500');
             passwordInput.classList.add('ring-border-light', 'dark:ring-slate-600', 'focus:ring-primary');
             if (formError) formError.classList.add('hidden');
        });
    }

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
                    // Inline error UI for Premium Feel
                    if (passwordHint) {
                        passwordHint.classList.remove('text-slate-500', 'dark:text-slate-400');
                        passwordHint.classList.add('text-red-500', 'dark:text-red-400', 'animate-pulse');
                        if (passwordHintIcon) passwordHintIcon.classList.remove('hidden');
                        if (passwordHintText) passwordHintText.textContent = 'Please make sure it is at least 8 characters with 1 special character.';
                    }
                    if (passwordInput) {
                        passwordInput.classList.remove('ring-border-light', 'dark:ring-slate-600', 'focus:ring-primary');
                        passwordInput.classList.add('ring-red-500', 'dark:ring-red-400', 'focus:ring-red-500');
                    }
                    return; // Stop form submission
                }
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
