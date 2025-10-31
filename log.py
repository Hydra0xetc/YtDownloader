import sys
from typing import Any

# fmt: off
## Text colors
BLACK      = "\033[30m"
RED        = "\033[31m"
GREEN      = "\033[32m"
YELLOW     = "\033[33m"
BLUE       = "\033[34m"
MAGENTA    = "\033[35m"
CYAN       = "\033[36m"
WHITE      = "\033[37m"

## Background colors
BG_BLACK   = "\033[40m"
BG_RED     = "\033[41m"
BG_GREEN   = "\033[42m"
BG_YELLOW  = "\033[43m"
BG_BLUE    = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN    = "\033[46m"
BG_WHITE   = "\033[47m"

## Text styles
DIM        = "\033[2m"
BOLD       = "\033[1m"
UNDERLINE  = "\033[4m"
BLINK      = "\033[5m"
REVERSE    = "\033[7m"

## Reset
RESET      = "\033[0m"

# fmt: on


def print_debug(message: Any) -> None:
    """Prints a colored [DEBUG] message to stderr.

    Args:
        message: The variable to be debugged.
    """
    print(f"{YELLOW}{BOLD}[DEBUG] {RESET}{message}", file=sys.stderr)


def print_error(message: Any) -> None:
    """Prints a colored [ERROR] message to stderr.

    Args:
        message: The variable to be included in the [ERROR] message.
    """
    print(f"{RED}{BOLD}[ERROR] {RESET}{message}", file=sys.stderr)


def print_warning(message: Any) -> None:
    """Prints a colored [WARNING] message to stderr.

    Args:
        message: The variable to be included in the [WARNING] message.
    """
    print(f"{MAGENTA}{BOLD}[WARNING] {RESET}{message}", file=sys.stderr)


def print_success(message: Any) -> None:
    """Prints a colored [SUCCESS] message to stdout.

    Args:
        message: The variable to be included in the [SUCCESS] message.
    """
    print(f"{GREEN}{BOLD}[SUCCESS] {RESET}{message}")