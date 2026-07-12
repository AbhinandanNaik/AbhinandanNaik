class Theme:
    def __init__(self, theme_name="cyberpunk"):
        self.theme_name = theme_name.lower()
        self.config = self._get_theme_config()
        
    def _get_theme_config(self):
        themes = {
            "cyberpunk": {
                "bg": "#090a0f",
                "bg_terminal": "#030508",
                "grid": "#141923",
                "grid_light": "#12161f",
                "primary": "#00f0ff",       # Cyan
                "secondary": "#ff007f",     # Neon Pink
                "accent": "#7000ff",        # Purple
                "status_ok": "#39ff14",     # Neon Green
                "status_warn": "#ffbd2e",    # Orange
                "text_primary": "#ffffff",
                "text_muted": "#8b949e",
                "text_blue": "#58a6ff"
            },
            "nord": {
                "bg": "#2e3440",
                "bg_terminal": "#242933",
                "grid": "#3b4252",
                "grid_light": "#4c566a",
                "primary": "#88c0d0",       # Frost Blue
                "secondary": "#bf616a",     # Red
                "accent": "#b48ead",        # Purple
                "status_ok": "#a3be8c",     # Green
                "status_warn": "#ebcb8b",    # Yellow
                "text_primary": "#eceff4",
                "text_muted": "#d8dee9",
                "text_blue": "#81a1c1"
            },
            "dracula": {
                "bg": "#282a36",
                "bg_terminal": "#1e1f29",
                "grid": "#44475a",
                "grid_light": "#6272a4",
                "primary": "#8be9fd",       # Cyan
                "secondary": "#ff79c6",     # Pink
                "accent": "#bd93f9",        # Purple
                "status_ok": "#50fa7b",     # Green
                "status_warn": "#f1fa8c",    # Yellow
                "text_primary": "#f8f8f2",
                "text_muted": "#6272a4",
                "text_blue": "#ffb86c"
            }
        }
        return themes.get(self.theme_name, themes["cyberpunk"])
        
    def get(self, key, default=None):
        return self.config.get(key, default)
