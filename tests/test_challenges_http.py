from pyshellgame.challenges.http import HealthCheckChallenge
from pyshellgame.session import GameSession


def test_health_check_challenge_passes_when_player_finds_the_healthy_endpoint():
    session = GameSession()
    challenge = HealthCheckChallenge()
    challenge.setup(session)

    session.run_command("curl /healthz")

    assert challenge.check_state(session)


def test_health_check_challenge_fails_when_player_only_hits_the_broken_endpoint():
    session = GameSession()
    challenge = HealthCheckChallenge()
    challenge.setup(session)

    session.run_command("curl /status")

    assert not challenge.check_state(session)
