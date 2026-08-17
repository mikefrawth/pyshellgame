from pyshellgame.challenges.http import WhoAmIChallenge
from pyshellgame.session import GameSession

PASSING_CODE = '''
def register_routes(session):
    from flask import jsonify

    app = session.app

    @app.get("/whoami")
    def whoami():
        return jsonify(role="engineer")
'''

FAILING_CODE = '''
def register_routes(session):
    from flask import jsonify

    app = session.app

    @app.get("/whoami")
    def whoami():
        return jsonify(role="intern")
'''


def test_whoami_challenge_passes_when_player_registers_a_correct_route():
    session = GameSession()
    challenge = WhoAmIChallenge()
    challenge.setup(session)
    session.challenge = challenge

    (session.workspace_dir / challenge.target_filename).write_text(PASSING_CODE)

    submit_result = session.run_command("submit")
    assert submit_result.success

    session.run_command("curl /whoami")

    assert challenge.check_state(session)
    assert session.is_challenge_completed(challenge.id)


def test_whoami_challenge_fails_when_player_registers_a_wrong_route():
    session = GameSession()
    challenge = WhoAmIChallenge()
    challenge.setup(session)
    session.challenge = challenge

    (session.workspace_dir / challenge.target_filename).write_text(FAILING_CODE)

    submit_result = session.run_command("submit")
    assert submit_result.success

    session.run_command("curl /whoami")

    assert not challenge.check_state(session)
    assert not session.is_challenge_completed(challenge.id)


def test_submit_reports_an_error_for_broken_player_code():
    session = GameSession()
    challenge = WhoAmIChallenge()
    challenge.setup(session)
    session.challenge = challenge

    (session.workspace_dir / challenge.target_filename).write_text("this is not valid python(")

    result = session.run_command("submit")

    assert not result.success
    assert "error" in result.output.lower()


def test_submit_on_a_non_file_editing_challenge_fails_clearly():
    session = GameSession()

    result = session.run_command("submit")

    assert not result.success
    assert "file-editing" in result.output


def test_setup_does_not_clobber_an_already_edited_workspace_file():
    session = GameSession()
    challenge = WhoAmIChallenge()
    challenge.setup(session)

    (session.workspace_dir / challenge.target_filename).write_text(PASSING_CODE)
    challenge.setup(session)  # e.g. re-running setup() on a relaunch

    assert (session.workspace_dir / challenge.target_filename).read_text() == PASSING_CODE


def test_help_tells_the_player_where_to_edit_the_file():
    session = GameSession()
    challenge = WhoAmIChallenge()
    challenge.setup(session)
    session.challenge = challenge

    result = session.run_command("help")

    assert str(session.workspace_dir / challenge.target_filename) in result.output
