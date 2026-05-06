"""
password_validator/demo.py

Shows the validator in action against a set of typical passwords.

Run modes:
  python demo.py              -- runs preset test cases
  python demo.py --interactive  -- lets you type your own password
"""

import sys
from validator import validate_password


def print_result(password: str, username: str = "", label: str = "") -> None:
    result = validate_password(password, username)
    strength = result["strength"]

    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    CYAN   = "\033[96m"
    RESET  = "\033[0m"
    BOLD   = "\033[1m"

    level_colour = {
        "Strong": GREEN,
        "Medium": YELLOW,
        "Weak":   RED,
    }.get(strength["level"], RESET)

    header = label or f'Password: "{password}"'
    if username:
        header += f"  (username: {username})"

    print(f"\n{BOLD}{CYAN}{'─' * 64}{RESET}")
    print(f"{BOLD}{header}{RESET}")
    print(
        f"  Strength : {level_colour}{BOLD}{strength['level']}{RESET}"
        f"  (score {strength['score']}/100)"
    )
    print(f"  Verdict  : {result['summary']}")

    if result["errors"]:
        print(f"\n  {RED}Errors (must fix):{RESET}")
        for e in result["errors"]:
            print(f"    - {e}")

    if result["warnings"]:
        print(f"\n  {YELLOW}Warnings:{RESET}")
        for w in result["warnings"]:
            print(f"    ~ {w}")

    print(f"\n  Breakdown:")
    for reason in strength["reasons"]:
        print(f"    {reason}")


# These cover every test case mentioned in the challenge spec.
DEMO_CASES = [
    # (password, username, label)
    ("abc",                  "",        "Too short"),
    ("onlylowercase",        "",        "Only lowercase"),
    ("12345678",             "",        "Only digits"),
    ("MixedCase",            "",        "Mixed case, no digits or specials"),
    ("password",             "",        "Common password (RockYou)"),
    ("iloveyou",             "",        "Another common password"),
    ("johndoe@2024!",        "johndoe", "Contains username"),
    ("aaaa1234!A",           "",        "Repeated characters"),
    ("Abcdef12345!",         "",        "Sequential letters and digits"),
    ("qwerty99!Ab",          "",        "Keyboard walk"),
    ("abcabcA1!",            "",        "Repeated chunk"),
    ("Summer2024!",          "",        "Passes rules but guessable (season+year)"),
    ("Tr0ub4dor&Bicycle#7!", "alice",   "Strong password"),
]


def run_demo() -> None:
    print("\n" + "=" * 64)
    print("  Password Strength Validator -- Demo")
    print("  Wordlist: RockYou top common passwords")
    print("=" * 64)

    for password, username, label in DEMO_CASES:
        print_result(password, username, label)

    print(f"\n{'─' * 64}\n")


def run_interactive() -> None:
    import getpass
    print("\n  Password Strength Validator -- Interactive")
    print("  Type 'quit' to exit.\n")
    while True:
        try:
            password = getpass.getpass("  Enter password (hidden): ")
            #aici avem hidden password in the interactive mode
        except (EOFError, KeyboardInterrupt):
            break
        if password.lower() in ("quit", "exit", "q"):
            break
        username = input("  Enter username (or press Enter to skip): ").strip()
        print_result(password, username)
    print("\n  Done.\n")


if __name__ == "__main__":
    if "--interactive" in sys.argv or "-i" in sys.argv:
        run_interactive()
    else:
        run_demo()
