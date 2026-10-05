import os
import sys
from pathlib import Path

from pilot_monitor import qt_compat


def test_wayland_kde6_uses_xcb_without_kde6_theme_state(monkeypatch):
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setenv("XDG_SESSION_TYPE", "wayland")
    monkeypatch.setenv("DISPLAY", ":0")
    monkeypatch.setenv("KDE_SESSION_VERSION", "6")
    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "KDE")
    monkeypatch.setenv("KDE_FULL_SESSION", "true")
    monkeypatch.setenv("DESKTOP_SESSION", "plasma")
    monkeypatch.delenv("QT_QPA_PLATFORM", raising=False)

    qt_compat.configure_qt_before_cv2_import()

    assert os.environ["QT_QPA_PLATFORM"] == "xcb"
    assert os.environ["XDG_CURRENT_DESKTOP"] == ""
    assert os.environ["KDE_FULL_SESSION"] == ""


def test_missing_wheel_font_directory_is_replaced(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "platform", "linux")
    missing = tmp_path / "missing-fonts"
    fallback = tmp_path / "fallback-fonts"
    fallback.mkdir()
    monkeypatch.setattr(qt_compat, "SYSTEM_QT_FONT_DIRS", (fallback,))
    monkeypatch.setenv("QT_QPA_FONTDIR", str(missing))

    qt_compat.configure_qt_fonts_after_cv2_import()

    configured = Path(os.environ["QT_QPA_FONTDIR"])
    assert configured.is_dir()
