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
