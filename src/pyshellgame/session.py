from dataclasses import dataclass


@dataclass(frozen=True)
class CommandResult:
    output: str
    success: bool = True


class GameSession:
    """Owns all player-facing game state and dispatches commands.

    `run_command` is the sole entry point for player action - the REPL and
    any future file-editing challenge flow both funnel through it.
    """

    def run_command(self, text: str) -> CommandResult:
        command = text.strip()
        if command == "help":
            return CommandResult(output="Available commands: help")
        return CommandResult(output=f"Unknown command: {command}", success=False)
