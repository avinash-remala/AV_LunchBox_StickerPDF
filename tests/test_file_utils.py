"""
Tests for file and directory utilities.
"""

import pytest
from pathlib import Path
from av_lunchbox_stickerpdf.utils.file_utils import (
    clean_directory,
    create_dated_export_dir,
    get_timestamp_filename,
    list_files_in_directory,
)


class TestCleanDirectory:
    """Tests for clean_directory()."""

    def test_clean_nonempty_directory(self, tmp_path):
        # Create some files and folders
        (tmp_path / "file1.txt").write_text("hello")
        (tmp_path / "file2.pdf").write_text("world")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "nested.txt").write_text("nested")

        result = clean_directory(str(tmp_path))
        assert result is True
        assert list(tmp_path.iterdir()) == []

    def test_clean_empty_directory(self, tmp_path):
        result = clean_directory(str(tmp_path))
        assert result is True

    def test_clean_nonexistent_directory(self):
        result = clean_directory("/nonexistent/path/abc123")
        assert result is False


class TestCreateDatedExportDir:
    """Tests for create_dated_export_dir()."""

    def test_creates_dated_directory(self, tmp_path):
        export_dir = create_dated_export_dir(str(tmp_path), "2026-02-20")
        assert export_dir.exists()
        assert export_dir.name == "2026-02-20"

    def test_creates_today_directory(self, tmp_path):
        from datetime import datetime
        export_dir = create_dated_export_dir(str(tmp_path))
        today = datetime.now().strftime("%Y-%m-%d")
        assert export_dir.name == today
        assert export_dir.exists()

    def test_idempotent(self, tmp_path):
        dir1 = create_dated_export_dir(str(tmp_path), "2026-02-20")
        dir2 = create_dated_export_dir(str(tmp_path), "2026-02-20")
        assert dir1 == dir2
        assert dir1.exists()


class TestGetTimestampFilename:
    """Tests for get_timestamp_filename()."""

    def test_pdf_extension(self):
        filename = get_timestamp_filename(".pdf")
        assert filename.endswith(".pdf")

    def test_txt_extension(self):
        filename = get_timestamp_filename(".txt")
        assert filename.endswith(".txt")

    def test_12h_format_default(self):
        filename = get_timestamp_filename(".pdf")
        # Should contain AM or PM
        assert "AM" in filename or "PM" in filename

    def test_24h_format(self):
        filename = get_timestamp_filename(".pdf", format_12h=False)
        # Should NOT contain AM/PM
        assert "AM" not in filename and "PM" not in filename

    def test_contains_date(self):
        from datetime import datetime
        filename = get_timestamp_filename(".pdf")
        today = datetime.now().strftime("%Y-%m-%d")
        assert today in filename


class TestListFilesInDirectory:
    """Tests for list_files_in_directory()."""

    def test_list_all_files(self, tmp_path):
        (tmp_path / "a.txt").write_text("a")
        (tmp_path / "b.pdf").write_text("b")
        (tmp_path / "c.txt").write_text("c")

        files = list_files_in_directory(str(tmp_path))
        assert len(files) == 3

    def test_filter_by_extension(self, tmp_path):
        (tmp_path / "a.txt").write_text("a")
        (tmp_path / "b.pdf").write_text("b")
        (tmp_path / "c.txt").write_text("c")

        files = list_files_in_directory(str(tmp_path), extension=".txt")
        assert len(files) == 2
        assert all(f.endswith(".txt") for f in files)

    def test_nonexistent_directory(self):
        files = list_files_in_directory("/nonexistent/path/abc123")
        assert files == []

    def test_excludes_subdirectories(self, tmp_path):
        (tmp_path / "file.txt").write_text("data")
        (tmp_path / "subdir").mkdir()

        files = list_files_in_directory(str(tmp_path))
        assert len(files) == 1
