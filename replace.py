import re

with open('frontends/securitycenter.html', 'r', encoding='utf-8') as f:
    text = f.read()

config_pattern = r'tailwind\.config = \{.*?\};'
new_config = '''tailwind.config = {
        darkMode: 'class',
        theme: {
          extend: {
            colors: {
              background: "#F3F4F6",
              "dark-background": "#0f172a",
              surface: "#ffffff",
              "dark-surface": "#1e293b",
              primary: "#000000",
              "dark-primary": "#ffffff",
              secondary: "#71717a",
              "dark-secondary": "#cbd5e1",
              border: "#e5e7eb",
              "dark-border": "#334155",
              brand: {
                DEFAULT: "#059669",
                dark: "#064e3b",
                light: "#d1fae5",
              },
              accent: {
                blue: "#1e40af",
                orange: "#ea580c",
              },
            },
            fontFamily: {
              sans: ["Inter", "sans-serif"],
            },
            boxShadow: {
              soft: "0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)",
              "dark-soft": "0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)",
            },
          },
        },
      };'''

text = re.sub(config_pattern, new_config, text, flags=re.DOTALL)

replacements = {
    'bg-background-light': 'bg-background',
    'dark:bg-background-dark': 'dark:bg-dark-background',
    'bg-surface-light': 'bg-surface',
    'dark:bg-surface-dark': 'dark:bg-dark-surface',
    'border-border-light': 'border-border',
    'dark:border-border-dark': 'dark:border-dark-border',
    'divide-border-light': 'divide-border',
    'dark:divide-border-dark': 'dark:divide-dark-border',
}

for k, v in replacements.items():
    text = text.replace(k, v)

with open('frontends/securitycenter.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done!")
