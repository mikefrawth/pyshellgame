from pyshellgame.session import GameSession


def main() -> None:
    session = GameSession()
    print("pyshellgame - type 'help' to get started, Ctrl+D to quit.")
    while True:
        try:
            text = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        result = session.run_command(text)
        print(result.output)


if __name__ == "__main__":
    main()
