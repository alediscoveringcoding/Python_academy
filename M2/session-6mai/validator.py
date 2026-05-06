"""
password_validator/validator.py

Checks password strength and returns structured feedback.
Designed to run before account creation -- not after.

Relies on rockyou_top.txt (common passwords from the RockYou breach)
to catch the low-hanging fruit that brute-force scripts try first.

Python 3.8+
"""

import re
from pathlib import Path


# Change these numbers if the rules need updating later.
# Everything else reads from this dict, so you won't have to hunt
# through the functions to adjust a threshold.
CONFIG = {
    "min_length": 8,
    "max_length": 128,
    "min_char_categories": 3,   # out of 4: lower, upper, digit, special
    "max_repeated_chars": 3,    # "aaaa" triggers at 4 in a row
    "max_sequential_chars": 3,  # "1234" triggers at 4 in a row
    # rockyou.txt should be in the same folder as this file.
    # Path(__file__).parent means "the folder this script is in",
    # so it works no matter where you run the script from.
    "wordlist_path": Path(__file__).parent / "rockyou.txt",
}


# ---------------------------------------------------------------------------
# Wordlist -- loaded once when the module is imported
# ---------------------------------------------------------------------------

def _load_wordlist(path: Path) -> set:
    # Tries to open the file at the given path.
    # If it's not there, the validator still runs -- it just skips the
    # common-password check and prints a warning so you know.
    if not path.exists():
        print(f"[WARNING] rockyou.txt not found at: {path}")
        print("[WARNING] Common-password check is disabled. Put rockyou.txt in the same folder as this script.")
        return set()
    with open(path, encoding="utf-8", errors="ignore") as f:
        words = {line.strip().lower() for line in f if line.strip()}
    print(f"[INFO] Loaded {len(words):,} passwords from {path.name}")
    return words


_COMMON_PASSWORDS: set = _load_wordlist(CONFIG["wordlist_path"])


# ---------------------------------------------------------------------------
# 1. check_length
# ---------------------------------------------------------------------------

def check_length(password: str) -> dict:
    """
    Check that the password is within an acceptable length range.

    Returns a dict:
        passed  (bool) - False means the password cannot be accepted
        message (str)  - reason, shown directly to the user
    """
    length = len(password)
    min_len = CONFIG["min_length"]
    max_len = CONFIG["max_length"]

    if length < min_len:
        return {
            "passed": False,
            "message": f"Too short ({length} chars). Minimum is {min_len}.",
        }

    if length > max_len:
        return {
            "passed": False,
            "message": f"Too long ({length} chars). Maximum is {max_len}.",
        }

    # Passes the hard rule but worth nudging the user toward something longer.
    if length < 12:
        return {
            "passed": True,
            "message": f"Length OK ({length} chars), but 12+ is recommended.",
        }

    return {
        "passed": True,
        "message": f"Good length ({length} chars).",
    }


# ---------------------------------------------------------------------------
# 2. check_character_types
# ---------------------------------------------------------------------------

def check_character_types(password: str) -> dict:
    """
    Check how many character categories the password uses.
    We want at least 3 of: lowercase, uppercase, digits, special chars.

    Returns a dict:
        passed     (bool) - True when enough categories are present
        categories (dict) - which ones were found
        missing    (list) - human-readable names of what is absent
        message    (str)  - summary for the user
    """
    categories = {
        "lowercase": bool(re.search(r"[a-z]", password)),
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "digits":    bool(re.search(r"\d", password)),
        "special":   bool(re.search(r"[^a-zA-Z\d]", password)),
    }

    # These labels go straight into the feedback message, so keep them readable.
    labels = {
        "lowercase": "lowercase letters (a-z)",
        "uppercase": "uppercase letters (A-Z)",
        "digits":    "digits (0-9)",
        "special":   "special characters (!@#$ etc.)",
    }

    missing = [labels[k] for k, found in categories.items() if not found]
    found_count = sum(categories.values())
    passed = found_count >= CONFIG["min_char_categories"]

    if passed:
        message = f"Good variety ({found_count}/4 categories present)."
    else:
        message = (
            f"Only {found_count}/4 categories present. "
            f"Missing: {', '.join(missing)}."
        )

    return {
        "passed": passed,
        "categories": categories,
        "missing": missing,
        "message": message,
    }


# ---------------------------------------------------------------------------
# 3. contains_common_password
# ---------------------------------------------------------------------------

def contains_common_password(password: str) -> dict:
    """
    Check whether the password shows up in the RockYou list.
    We compare lowercase so "Password" and "PASSWORD" both get caught.

    Returns a dict:
        passed  (bool) - True means it is NOT a known common password
        message (str)
    """
    if not _COMMON_PASSWORDS:
        return {"passed": True, "message": "Common-password check skipped (no wordlist)."}

    if password.lower() in _COMMON_PASSWORDS:
        return {
            "passed": False,
            "message": "This password is in the list of most-used passwords and would be guessed immediately.",
        }

    return {
        "passed": True,
        "message": "Not found in common-password list.",
    }


# ---------------------------------------------------------------------------
# 4. contains_personal_info
# ---------------------------------------------------------------------------

def contains_personal_info(password: str, username: str) -> dict:
    """
    Check whether the password contains the username or a chunk of it.
    Users do this constantly -- "johndoe2024!" is not a real password.

    We check substrings down to 4 characters so partial matches like
    "alex" inside "alexander" are still caught.

    Returns a dict:
        passed  (bool)
        message (str)
    """
    if not username:
        return {"passed": True, "message": "No username provided -- personal-info check skipped."}

    pw_lower = password.lower()
    user_lower = username.lower()

    if user_lower in pw_lower:
        return {
            "passed": False,
            "message": f"Password contains the username '{username}'. Choose something unrelated.",
        }

    # Walk every substring of the username that is 4+ chars long.
    for length in range(4, len(user_lower) + 1):
        for start in range(len(user_lower) - length + 1):
            chunk = user_lower[start : start + length]
            if chunk in pw_lower:
                return {
                    "passed": False,
                    "message": (
                        f"Password contains part of the username ('{chunk}'). "
                        "Avoid using personal information."
                    ),
                }

    return {
        "passed": True,
        "message": "No personal information detected.",
    }


# ---------------------------------------------------------------------------
# 5. has_repeated_or_sequential_patterns
# ---------------------------------------------------------------------------

def has_repeated_or_sequential_patterns(password: str) -> dict:
    """
    Look for patterns that make a password easy to guess even if it
    technically passes the length and variety checks.

    Things we check for:
      - same character repeated too many times  (aaaa, 1111)
      - ascending or descending sequences       (1234, abcd, 9876)
      - a chunk that repeats back-to-back       (abcabc, 123123)
      - known keyboard walks                    (qwerty, asdf)

    Returns a dict:
        passed   (bool)
        patterns (list) - description of each bad pattern found
        message  (str)
    """
    patterns_found = []
    pw_lower = password.lower()
    max_rep = CONFIG["max_repeated_chars"]
    max_seq = CONFIG["max_sequential_chars"]

    # Build the regex at runtime so max_rep is respected from CONFIG.
    repeat_re = re.compile(r"(.)\1{" + str(max_rep) + r",}")
    if repeat_re.search(password):
        patterns_found.append("Long run of the same character (e.g. 'aaaa', '1111').")

    def _has_sequence(text: str, max_len: int) -> bool:
        # Slide a window across the string and check whether every
        # consecutive pair has the same step (+1 or -1).
        for i in range(len(text) - max_len):
            window = text[i : i + max_len + 1]
            codes = [ord(c) for c in window]
            diffs = [codes[j + 1] - codes[j] for j in range(len(codes) - 1)]
            if all(d == 1 for d in diffs) or all(d == -1 for d in diffs):
                return True
        return False

    if _has_sequence(pw_lower, max_seq):
        patterns_found.append("Sequential pattern detected (e.g. '1234', 'abcd', '9876').")

    # Check every possible chunk length from 2 up to half the password length.
    # If any chunk appears twice in a row, flag it and stop -- one report is enough.
    for chunk_len in range(2, len(password) // 2 + 1):
        for start in range(len(password) - chunk_len * 2 + 1):
            chunk = password[start : start + chunk_len]
            if chunk == password[start + chunk_len : start + chunk_len * 2]:
                patterns_found.append(f"Repeated chunk detected ('{chunk}' appears back-to-back).")
                break
        else:
            continue
        break

    keyboard_patterns = [
        "qwerty", "qwertyuiop", "asdfgh", "asdfghjkl",
        "zxcvbn", "zxcvbnm", "1qaz2wsx", "qazwsx",
        "!qaz", "1qaz", "qweasd",
    ]
    for kp in keyboard_patterns:
        if kp in pw_lower:
            patterns_found.append(f"Keyboard walk pattern detected ('{kp}').")
            break

    if patterns_found:
        return {
            "passed": False,
            "patterns": patterns_found,
            "message": "Weak patterns found: " + " | ".join(patterns_found),
        }

    return {
        "passed": True,
        "patterns": [],
        "message": "No repeated or sequential patterns detected.",
    }


# ---------------------------------------------------------------------------
# 6. calculate_strength
# ---------------------------------------------------------------------------

def calculate_strength(password: str, username: str = "") -> dict:
    """
    Run all sub-checks and roll them up into a single score and level.

    Scoring breakdown (max 100):
      length passes          +20
      3 char categories      +20,  4 categories  +30
      not a common password  +20   (if it IS common, score is forced to 0)
      no personal info       +10   (username in password = -20 penalty)
      no weak patterns       +20

    Levels:
      0-39  -> Weak
      40-69 -> Medium
      70+   -> Strong

    Returns a dict:
        score   (int)  0-100
        level   (str)  "Weak" | "Medium" | "Strong"
        reasons (list) one line per check explaining the score
    """
    score = 0
    reasons = []

    length_result = check_length(password)
    if length_result["passed"]:
        score += 20
        reasons.append("+ Length is acceptable.")
    else:
        reasons.append(f"- {length_result['message']}")

    char_result = check_character_types(password)
    count = sum(char_result["categories"].values())
    if count == 4:
        score += 30
        reasons.append("+ All 4 character categories present.")
    elif count == 3:
        score += 20
        reasons.append("+ 3 character categories present.")
    elif count == 2:
        score += 10
        reasons.append("~ Only 2 character categories (limited variety).")
    else:
        reasons.append("- Only 1 character category (very weak variety).")

    # If the password is on the common list we set the score to zero and
    # return early -- there is no point scoring the other checks.
    common_result = contains_common_password(password)
    if common_result["passed"]:
        score += 20
        reasons.append("+ Not a known common password.")
    else:
        reasons.append("- Found in common-password list.")
        return {"score": 0, "level": "Weak", "reasons": reasons}

    personal_result = contains_personal_info(password, username)
    if personal_result["passed"]:
        score += 10
        reasons.append("+ No personal information detected.")
    else:
        score = max(0, score - 20)
        reasons.append(f"~ {personal_result['message']}")

    pattern_result = has_repeated_or_sequential_patterns(password)
    if pattern_result["passed"]:
        score += 20
        reasons.append("+ No weak patterns detected.")
    else:
        reasons.append(f"- Weak pattern: {'; '.join(pattern_result['patterns'])}")

    if score >= 70:
        level = "Strong"
    elif score >= 40:
        level = "Medium"
    else:
        level = "Weak"

    return {"score": score, "level": level, "reasons": reasons}


# ---------------------------------------------------------------------------
# 7. validate_password -- the main entry point
# ---------------------------------------------------------------------------

def validate_password(password: str, username: str = "") -> dict:
    """
    Run every check and return a single result dict that the rest of the
    app can use to decide whether to accept the password.

    Hard errors go into 'errors' -- the password cannot be accepted.
    Soft issues go into 'warnings' -- the password passes but the user
    should be told about the problem.

    Parameters:
        password (str) - the password to check
        username (str) - optional, used for the personal-info check

    Returns a dict:
        valid        (bool)       - False if any hard error was found
        errors       (list[str])  - things that must be fixed
        warnings     (list[str])  - things worth flagging to the user
        requirements (dict)       - pass/fail for each individual check
        strength     (dict)       - score, level, and breakdown reasons
        summary      (str)        - one-line verdict for display
    """
    errors = []
    warnings = []
    requirements = {}

    length = check_length(password)
    requirements["length"] = length["passed"]
    if not length["passed"]:
        errors.append(length["message"])
    elif "recommended" in length["message"]:
        warnings.append(length["message"])

    chars = check_character_types(password)
    requirements["character_variety"] = chars["passed"]
    if not chars["passed"]:
        errors.append(chars["message"])

    common = contains_common_password(password)
    requirements["not_common"] = common["passed"]
    if not common["passed"]:
        errors.append(common["message"])

    # Personal info is a warning, not a hard blocker.
    # The caller might not have a username to pass in.
    personal = contains_personal_info(password, username)
    requirements["no_personal_info"] = personal["passed"]
    if not personal["passed"]:
        warnings.append(personal["message"])

    # Same for patterns they lower the score but don't outright block.
    pattern = has_repeated_or_sequential_patterns(password)
    requirements["no_weak_patterns"] = pattern["passed"]
    if not pattern["passed"]:
        warnings.append(pattern["message"])

    strength = calculate_strength(password, username)

    if strength["level"] == "Weak" and not errors:
        warnings.append("Overall strength is Weak -- consider a stronger password.")

    valid = len(errors) == 0

    if valid and strength["level"] == "Strong":
        summary = "Password is strong and ready to use."
    elif valid and strength["level"] == "Medium":
        summary = "Password is acceptable but could be stronger."
    elif valid:
        summary = "Password meets the minimum rules but is weak."
    else:
        summary = "Password failed validation and cannot be accepted."

    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "requirements": requirements,
        "strength": strength,
        "summary": summary,
    }
