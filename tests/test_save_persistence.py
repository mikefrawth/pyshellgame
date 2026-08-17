from pathlib import Path

from pyshellgame.session import GameSession


def test_completing_challenge_updates_save_file(tmp_path: Path):
    save_path = tmp_path / "save.json"
    session = GameSession(save_path=save_path)

    session.run_command("curl /healthz")

    assert session.is_challenge_completed("chapter1-healthcheck")
    assert save_path.exists()


def test_relaunching_loads_prior_completion(tmp_path: Path):
    save_path = tmp_path / "save.json"
    first_session = GameSession(save_path=save_path)
    first_session.run_command("curl /healthz")

    second_session = GameSession(save_path=save_path)

    assert second_session.is_challenge_completed("chapter1-healthcheck")


def test_fresh_save_starts_with_no_completions_and_does_not_error(tmp_path: Path):
    save_path = tmp_path / "does-not-exist" / "save.json"

    session = GameSession(save_path=save_path)

    assert not session.is_challenge_completed("chapter1-healthcheck")
