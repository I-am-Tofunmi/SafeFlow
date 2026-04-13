/**
 * SafeFlow Global Theme Manager
 * Handles dark/light mode persistence and UI synchronization.
 */

(function() {
    // 1. Immediate Theme Application (to prevent flicker)
    const savedTheme = localStorage.getItem('safeflow-theme');
    
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }

    // 2. Theme Initialization
    window.addEventListener('DOMContentLoaded', () => {
        initializeThemeToggle();
    });

    function initializeThemeToggle() {
        const themeToggles = document.querySelectorAll('#theme-toggle, .theme-toggle-btn');
        
        themeToggles.forEach(toggle => {
            const icon = toggle.querySelector('.material-symbols-outlined, .material-icons-outlined');
            
            // Sync icon state
            updateIcon(icon);

            toggle.addEventListener('click', () => {
                const isDark = document.documentElement.classList.toggle('dark');
                localStorage.setItem('safeflow-theme', isDark ? 'dark' : 'light');
                updateIcon(icon);
                
                // Broadcast theme change to other open tabs
                window.dispatchEvent(new Event('themeChanged'));
            });
        });
    }

    function updateIcon(icon) {
        if (!icon) return;
        const isDark = document.documentElement.classList.contains('dark');
        icon.textContent = isDark ? 'light_mode' : 'dark_mode';
    }

    // 3. Listen for theme changes from other tabs
    window.addEventListener('storage', (e) => {
        if (e.key === 'safeflow-theme') {
            if (e.newValue === 'dark') {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }
            const icons = document.querySelectorAll('#theme-toggle .material-symbols-outlined, .theme-toggle-btn .material-symbols-outlined');
            icons.forEach(updateIcon);
        }
    });

    // 4. Keyboard Shortcut (Ctrl/Cmd + T)
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 't') {
            e.preventDefault();
            const firstToggle = document.querySelector('#theme-toggle, .theme-toggle-btn');
            if (firstToggle) firstToggle.click();
        }
    });
})();
