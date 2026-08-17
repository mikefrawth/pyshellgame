from pyshellgame.challenge import Challenge, FileEditingChallenge


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


class WhoAmIChallenge(FileEditingChallenge):
    """Chapter 1 (file-editing): register a `/whoami` diagnostic route.

    The player edits `whoami_route.py` in their workspace to define
    `register_routes(session)`. `submit` loads that file and calls
    `register_routes(session)` against the live Flask app; the player then
    hits the new route with `curl` to complete the challenge."""

    id = "chapter1-whoami-route"
    target_filename = "whoami_route.py"
    entry_point = "register_routes"
    hints = [
        'You need to register a new route on the real Flask app - it\'s available as `session.app` inside `register_routes`.',
        'Use `@app.get("/whoami")` inside `register_routes(session)` to add the route.',
        'The route should return HTTP 200 with a JSON body like {"role": "engineer"} - try `from flask import jsonify`.',
    ]

    STARTER_CODE = '''"""Player-edited file for the /whoami challenge.

Add a GET /whoami route to the live Flask app that returns
{"role": "engineer"} with a 200 status, then run `submit` and `curl /whoami`.
"""


def register_routes(session):
    app = session.app
    # TODO: register a GET /whoami route on `app` that returns
    # jsonify(role="engineer")
'''

    def setup(self, session) -> None:
        session.write_workspace_file(self.target_filename, self.STARTER_CODE)

    def check_state(self, session) -> bool:
        response = session.last_http_response
        if response is None:
            return False
        return response.status_code == 200 and response.get_json() == {"role": "engineer"}
