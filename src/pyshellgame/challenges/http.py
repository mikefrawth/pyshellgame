from pyshellgame.challenge import Challenge


class HealthCheckChallenge(Challenge):
    """Chapter 1: diagnose the broken `/status` endpoint and find the
    real health-check endpoint (`/healthz`) that reports the app is up."""

    id = "chapter1-healthcheck"
    hints = [
        "The `/status` endpoint exists, but is it the one a real health check would use?",
        "A proper health-check endpoint should return HTTP 200 with a JSON body like {\"status\": \"ok\"}.",
        "Try `curl /healthz`.",
    ]

    def setup(self, session) -> None:
        pass  # the app is already wired with the broken /status endpoint

    def check_state(self, session) -> bool:
        response = session.last_http_response
        if response is None:
            return False
        return response.status_code == 200 and response.get_json() == {"status": "ok"}
