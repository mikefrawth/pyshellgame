import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from werkzeug.test import TestResponse

from pyshellgame.app import create_app
from pyshellgame.challenge import FileEditingChallenge
from pyshellgame.challenges.http import HealthCheckChallenge
from pyshellgame.save import (
    default_save_path,
    load_completed_challenges,
    write_completed_challenges,
)

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

    def __init__(self, save_path: Optional[Path] = None) -> None:
        self.app = create_app()
        self.client = self.app.test_client()
        self.last_http_response: Optional[TestResponse] = None

        self.save_path = Path(save_path) if save_path is not None else default_save_path()
        self.completed_challenges: set[str] = load_completed_challenges(self.save_path)
        self.workspace_dir = self.save_path.parent / "workspace"

        self.challenge = HealthCheckChallenge()
        self.challenge.setup(self)
        self._hint_level = -1

    def run_command(self, text: str) -> CommandResult:
        command = text.strip()
        parts = command.split()
        if not parts:
            return CommandResult(output="", success=False)

        verb, args = parts[0], parts[1:]
        if verb == "help":
            result = CommandResult(output=self._help_text())
        elif verb == "curl":
            result = self._run_curl(args)
        elif verb == "hint":
            result = self._run_hint()
        elif verb == "submit":
            result = self._run_submit()
        else:
            result = CommandResult(output=f"Unknown command: {command}", success=False)

        self._check_challenge_completion()
        return result

    def is_challenge_completed(self, challenge_id: str) -> bool:
        return challenge_id in self.completed_challenges

    def _check_challenge_completion(self) -> None:
        if self.is_challenge_completed(self.challenge.id):
            return
        if self.challenge.check_state(self):
            self.completed_challenges.add(self.challenge.id)
            write_completed_challenges(self.save_path, self.completed_challenges)

    def _run_hint(self) -> CommandResult:
        hints = self.challenge.hints
        if not hints:
            return CommandResult(output="No hints available for this challenge.")

        self._hint_level = min(self._hint_level + 1, len(hints) - 1)
        return CommandResult(output=hints[self._hint_level])

    def _help_text(self) -> str:
        text = "Available commands: help, curl, hint, submit"
        if isinstance(self.challenge, FileEditingChallenge):
            target_path = self.workspace_dir / self.challenge.target_filename
            text += f"\nEdit {target_path}, then run `submit`."
        return text

    def write_workspace_file(self, filename: str, content: str) -> Path:
        """Write a starter file into the player's workspace, unless the
        player has already edited it (so re-running setup() doesn't clobber
        in-progress work)."""
        path = self.workspace_dir / filename
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        return path

    def load_player_module(self, filename: str):
        """Load the player-edited file at `workspace_dir/filename` as a
        Python module and return it."""
        path = self.workspace_dir / filename
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"could not load player module from {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _run_submit(self) -> CommandResult:
        if not isinstance(self.challenge, FileEditingChallenge):
            return CommandResult(
                output="submit: the current challenge isn't a file-editing challenge.",
                success=False,
            )
        try:
            self.challenge.run_player_code(self)
        except Exception as exc:
            return CommandResult(
                output=f"submit: error running your code: {exc}", success=False
            )
        return CommandResult(output="Submitted. Your code loaded and ran successfully.")

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
