class Challenge:
    """Base class for game challenges.

    Subclasses must not call input()/print() or otherwise touch terminal
    I/O - that belongs exclusively to the CLI presentation layer.
    """

    def setup(self, session) -> None:
        raise NotImplementedError

    def check_state(self, session) -> bool:
        raise NotImplementedError
