from flask import Flask, jsonify


def create_app() -> Flask:
    """Build the in-game Flask app the player's shell commands run against.

    Routes here are in-game content, not framework scaffolding - e.g.
    `/status` is deliberately broken to give chapter 1 something to diagnose.
    """
    app = Flask(__name__)

    @app.get("/healthz")
    def healthz():
        return jsonify(status="ok")

    @app.get("/status")
    def status():
        # Intentionally broken: chapter 1 teaching content, not a bug to fix here.
        return jsonify(error="internal error"), 500

    return app
