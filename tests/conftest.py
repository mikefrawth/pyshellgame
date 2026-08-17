import pytest

import pyshellgame.session as session_module


@pytest.fixture(autouse=True)
def isolate_default_save_path(tmp_path, monkeypatch):
    """Prevent tests that don't pass save_path explicitly from touching
    the real user's ~/.pyshellgame save file."""
    monkeypatch.setattr(
        session_module, "default_save_path", lambda: tmp_path / "save.json"
    )
