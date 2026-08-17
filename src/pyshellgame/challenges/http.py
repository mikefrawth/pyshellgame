from pyshellgame.challenge import Challenge


class HealthCheckChallenge(Challenge):
    """Chapter 1: diagnose the broken `/status` endpoint and find the
    real health-check endpoint (`/healthz`) that reports the app is up."""

    def setup(self, session) -> None:
        pass  # the app is already wired with the broken /status endpoint

    def check_state(self, session) -> bool:
        response = session.last_http_response
        if response is None:
            return False
        return response.status_code == 200 and response.get_json() == {"status": "ok"}
