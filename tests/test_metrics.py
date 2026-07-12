import unittest
import os
import sys

# Add root folder to python path to support execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.git_analyzer import GitAnalyzer
from src.render.theme import Theme
from src.main import load_config

class TestTelemetryMetrics(unittest.TestCase):
    def test_git_analyzer_fallback(self):
        # When analyzer runs on an invalid path, it should safely return fallback metrics
        analyzer = GitAnalyzer(repo_path="invalid_path_test_foo_bar")
        stats = analyzer.analyze_commits()
        self.assertIn("features", stats)
        self.assertIn("bugfixes", stats)
        self.assertEqual(stats["features"], 38)
        
    def test_theme_resolution(self):
        theme_cyber = Theme("cyberpunk")
        theme_nord = Theme("nord")
        theme_invalid = Theme("invalid_theme_name_fallback")
        
        self.assertEqual(theme_cyber.get("primary"), "#00f0ff")
        self.assertEqual(theme_nord.get("primary"), "#88c0d0")
        # Should fallback to cyberpunk if key invalid
        self.assertEqual(theme_invalid.get("primary"), "#00f0ff")
        
    def test_load_config_fallback(self):
        config = load_config("non_existent_config.json")
        self.assertEqual(config["github_username"], "AbhinandanNaik")
        self.assertTrue(config["features"]["leetcode"])

if __name__ == "__main__":
    unittest.main()
