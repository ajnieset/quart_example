import sys
from subprocess import CalledProcessError, check_call


def _check_call_quiet(commands: list[str], *, shell: bool = False) -> None:
    try:
        check_call(commands, shell=shell)
    except CalledProcessError as error:
        sys.exit(error.returncode)


def start() -> None:
    _check_call_quiet(["python", "src/quart_example/app.py"])


def test() -> None:
    _check_call_quiet(["pytest", "tests/"])
