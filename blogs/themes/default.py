DEFAULT_THEME = """:root {
  color-scheme: light dark;

  --background-color: #ffffff;
  --link-color: blue;
  --text-color: #213547;

  color: var(--text-color);
  background-color: var(--background-color);
}

html {
  box-sizing: border-box;
  font-family:
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    Oxygen,
    Ubuntu,
    Cantarell,
    "Open Sans",
    "Helvetica Neue",
    sans-serif;
  line-height: 1.5;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text-color);
  background-color: var(--background-color);
}

*,
::after,
::before {
  box-sizing: inherit;
  text-decoration-thickness: 0.2rem;
}

body {
  max-width: 740px;
  margin: auto;
}

a {
  color: var(--link-color);
  text-decoration: none;
}

@media (prefers-color-scheme: dark) {
  :root {
    color-scheme: light dark;

    --background-color: #ffffff;
    --text-color: #213547;
    --link-color: blue;

    color: var(--text-color);
    background-color: var(--background-color);
  }
}"""


DEFAULT_MUSIC_PLAYER_THEME = """:host {
  --background: white;
  --text-color: black;
  --border-color: black;
  --button-background: white;
  --button-fill-color: black;
  --slider-background: black;
  --thumb-background: white;
  --box-shadow-color-primary: black;
  --box-shadow-color-secondary: #0d0d0d;
  --font-family: monospace;
}"""
