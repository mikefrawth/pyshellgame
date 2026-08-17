from dataclasses import dataclass
from typing import Optional

from werkzeug.test import TestResponse

from pyshellgame.app import create_app

HTTP_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}


@dataclass(frozen=True)
class CommandResult:
    output: str
    success: bool = True


class GameSession:
    """Owns all player-facing game state and dispatches commands.

    `run_command` is the sole entry point for player action - the REPL and
    any future file-editing challenge flow both funnel through it.
    """

    def __init__(self) -> None:
        self.app = create_app()
        self.client = self.app.test_client()
        self.last_http_response: Optional[TestResponse] = None

    def run_command(self, text: str) -> CommandResult:
        command = text.strip()
        parts = command.split()
        if not parts:
            return CommandResult(output="", success=False)

        verb, args = parts[0], parts[1:]
        if verb == "help":
            return CommandResult(output="Available commands: help, curl")
        if verb == "curl":
            return self._run_curl(args)
        return CommandResult(output=f"Unknown command: {command}", success=False)

    def _run_curl(self, args: list[str]) -> CommandResult:
        if not args:
            return CommandResult(output="curl: missing URL", success=False)

        method = "GET"
        path = args[0]
        if len(args) >= 2 and args[0].upper() in HTTP_METHODS:
            method = args[0].upper()
            path = args[1]

        response = self.client.open(path, method=method)
        self.last_http_response = response
        body = response.get_data(as_text=True)
        return CommandResult(output=f"HTTP {response.status_code}\n{body}")
