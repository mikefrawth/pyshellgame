from pyshellgame.session import GameSession


def test_help_command_succeeds_and_lists_commands():
    session = GameSession()

    result = session.run_command("help")

    assert result.success
    assert "help" in result.output.lower()


def test_unknown_command_fails_with_message():
    session = GameSession()

    result = session.run_command("frobnicate")

    assert not result.success
    assert "frobnicate" in result.output


def test_curl_hits_the_real_flask_app():
    session = GameSession()

    result = session.run_command("curl /healthz")

    assert result.success
    assert "200" in result.output


def test_hint_progresses_through_levels_and_holds_on_the_last():
    session = GameSession()
    expected_hints = session.challenge.hints

    seen = [session.run_command("hint").output for _ in range(len(expected_hints) + 2)]

    assert seen[: len(expected_hints)] == expected_hints
    assert seen[len(expected_hints) - 1] == seen[-1]


def test_hint_does_not_affect_challenge_completion():
    session = GameSession()

    session.run_command("hint")

    assert not session.is_challenge_completed(session.challenge.id)
