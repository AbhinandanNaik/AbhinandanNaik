import json
import os
import sys

# Add current directory to path to support running from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.metrics_engine import MetricsEngine
from src.render.theme import Theme
from src.render.svg_generator import SvgGenerator

def load_config(config_path="config.json"):
    if not os.path.exists(config_path):
        print(f"Config file not found at {config_path}. Loading defaults.")
        return {
            "github_username": "AbhinandanNaik",
            "leetcode_username": "AbhinandanNaik",
            "theme": "cyberpunk",
            "features": {
                "git_analyzer": True,
                "leetcode": True,
                "kubernetes_console": True,
                "stats_dashboard": True,
                "contribution_matrix": True
            }
        }
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error parsing config file: {e}. Loading defaults.")
        return {
            "github_username": "AbhinandanNaik",
            "leetcode_username": "AbhinandanNaik",
            "theme": "cyberpunk",
            "features": {
                "git_analyzer": True,
                "leetcode": True,
                "kubernetes_console": True,
                "stats_dashboard": True,
                "contribution_matrix": True
            }
        }

def main():
    print("Initializing Enterprise Developer Telemetry Build Pipeline...")
    config = load_config()
    
    # 1. Collect all statistics
    engine = MetricsEngine(config)
    metrics_payload = engine.collect_all_metrics()
    
    # 2. Initialise Theme
    theme_name = config.get("theme", "cyberpunk")
    theme = Theme(theme_name)
    print(f"Theme loaded: {theme_name.upper()}")
    
    # 3. Generate SVGs
    generator = SvgGenerator(metrics_payload, theme)
    generator.generate_all()
    print("All enterprise dashboard SVG views successfully rendered in 'assets/'!")

if __name__ == "__main__":
    main()
