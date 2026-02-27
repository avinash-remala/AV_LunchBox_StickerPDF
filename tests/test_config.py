"""
Tests for AppConfig.
"""

from pathlib import Path
from av_lunchbox_stickerpdf.config.app_config import AppConfig


class TestAppConfig:
    """Tests for AppConfig settings."""

    def test_project_root_exists(self):
        assert AppConfig.PROJECT_ROOT.exists()

    def test_default_template_path(self):
        template = AppConfig.DEFAULT_TEMPLATE
        assert template.name == "AR_Template.docx"
        assert "templates" in str(template)

    def test_exports_dir(self):
        assert AppConfig.EXPORTS_DIR.name == "exports"

    def test_ensure_directories(self):
        AppConfig.ensure_directories()
        assert AppConfig.EXPORTS_DIR.exists()
        assert AppConfig.TEMPLATES_DIR.exists()

    def test_get_template_path_default(self):
        path = AppConfig.get_template_path()
        assert path == AppConfig.DEFAULT_TEMPLATE

    def test_get_template_path_custom(self):
        path = AppConfig.get_template_path("Custom.docx")
        assert path.name == "Custom.docx"

    def test_get_export_dir_with_date(self):
        path = AppConfig.get_export_dir("2026-02-20")
        assert path.name == "2026-02-20"

    def test_get_export_dir_today(self):
        from datetime import datetime
        path = AppConfig.get_export_dir()
        today = datetime.now().strftime("%Y-%m-%d")
        assert path.name == today
