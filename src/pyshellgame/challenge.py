class Challenge:
    """Base class for game challenges.

    Subclasses must not call input()/print() or otherwise touch terminal
    I/O - that belongs exclusively to the CLI presentation layer.
    """

    id: str
    hints: list[str] = []

    def setup(self, session) -> None:
        raise NotImplementedError

    def check_state(self, session) -> bool:
        raise NotImplementedError


class FileEditingChallenge(Challenge):
    """A challenge solved by editing a real file rather than the REPL.

    `target_filename` names the file (relative to the session's workspace
    directory) the player edits. `entry_point` names the module-level
    function in that file which the game calls, passing the live
    `GameSession`, when the player runs `submit`. Grading still goes
    through the same `check_state()` as any other challenge - `submit`
    only runs the player's code, it doesn't grade it.
    """

    target_filename: str
    entry_point: str

    def run_player_code(self, session) -> None:
        module = session.load_player_module(self.target_filename)
        entry = getattr(module, self.entry_point)
        entry(session)
