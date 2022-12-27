from sparrow_cli.api import app
import sparrow_cli.api.new
import sparrow_cli.api.callback
import sparrow_cli.api.version
from sparrow_cli.consoles import console

def main():  # pragma: no cover
    """CLI's main function."""
    console.rule("Welcome to the Sparrow CLI :robot:")
    console.print()
    try:
        app()
    finally:
        console.rule("See you later! :call_me_hand:")
        console.print()


if __name__ == "__main__":
    main()
