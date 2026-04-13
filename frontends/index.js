// Signup Form Submission Handler
document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');
    const signupButton = document.getElementById('signupButton');
    const buttonText = document.getElementById('buttonText');
    const buttonIcon = document.getElementById('buttonIcon');
    const loader = document.getElementById('loader');

    if (signupForm && signupButton) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
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
