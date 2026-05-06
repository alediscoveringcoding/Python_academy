"""
password_validator/tests.py

Covers every function in validator.py.
No external libraries needed -- just run: python tests.py
"""

from validator import (
    check_length,
    check_character_types,
    contains_common_password,
    contains_personal_info,
    has_repeated_or_sequential_patterns,
    calculate_strength,
    validate_password,
)

# ---------------------------------------------------------------------------
# Minimal test harness
# ---------------------------------------------------------------------------

_passed = 0
_failed = 0


def assert_true(condition: bool, test_name: str, hint: str = "") -> None:
    global _passed, _failed
    if condition:
        print(f"  PASS  {test_name}")
        _passed += 1
    else:
        msg = f"  FAIL  {test_name}"
        if hint:
            msg += f"  ->  {hint}"
        print(msg)
        _failed += 1


def section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# 1. check_length
# ---------------------------------------------------------------------------

section("check_length")

r = check_length("abc")
assert_true(not r["passed"], "Short password fails", r["message"])

r = check_length("a" * 200)
assert_true(not r["passed"], "Over-long password fails", r["message"])

r = check_length("Tr0ub4dor")
assert_true(r["passed"], "9-char password passes (with a note)", r["message"])

r = check_length("Tr0ub4dor&Bicycle")
assert_true(r["passed"], "17-char password passes cleanly", r["message"])


# ---------------------------------------------------------------------------
# 2. check_character_types
# ---------------------------------------------------------------------------

section("check_character_types")

r = check_character_types("alllower")
assert_true(not r["passed"], "Only lowercase fails", r["message"])

r = check_character_types("12345678")
assert_true(not r["passed"], "Only digits fails", r["message"])

r = check_character_types("MixedCase1")
assert_true(r["passed"], "Upper + lower + digit passes (3 categories)", r["message"])

r = check_character_types("G00dP@ss!")
assert_true(r["passed"], "All 4 categories passes", r["message"])
assert_true(all(r["categories"].values()), "All category flags are True for 'G00dP@ss!'")

r = check_character_types("hello")
assert_true(
    any("uppercase" in item for item in r["missing"]),
    "Missing uppercase is reported in the missing list",
    str(r["missing"]),
)


# ---------------------------------------------------------------------------
# 3. contains_common_password
# ---------------------------------------------------------------------------

section("contains_common_password")

r = contains_common_password("password")
assert_true(not r["passed"], "'password' detected as common", r["message"])

r = contains_common_password("PASSWORD")
assert_true(not r["passed"], "'PASSWORD' still detected (case-insensitive)", r["message"])

r = contains_common_password("iloveyou")
assert_true(not r["passed"], "'iloveyou' detected as common", r["message"])

r = contains_common_password("Tr0ub4dor&Bicycle#7!")
assert_true(r["passed"], "Strong unique password not in common list", r["message"])

r = contains_common_password("123456")
assert_true(not r["passed"], "'123456' detected as common", r["message"])


# ---------------------------------------------------------------------------
# 4. contains_personal_info
# ---------------------------------------------------------------------------

section("contains_personal_info")

r = contains_personal_info("johndoe2024!", "johndoe")
assert_true(not r["passed"], "Password with full username fails", r["message"])

r = contains_personal_info("JohnDoe2024!", "johndoe")
assert_true(not r["passed"], "Case-insensitive username match fails", r["message"])

r = contains_personal_info("secureP@ss99!", "johndoe")
assert_true(r["passed"], "Password with no personal info passes", r["message"])

r = contains_personal_info("myalex123!", "alexander")
assert_true(not r["passed"], "Partial username match (4+ chars) fails", r["message"])

r = contains_personal_info("superPass1!", "")
assert_true(r["passed"], "Empty username -- check skipped, passes", r["message"])


# ---------------------------------------------------------------------------
# 5. has_repeated_or_sequential_patterns
# ---------------------------------------------------------------------------

section("has_repeated_or_sequential_patterns")

r = has_repeated_or_sequential_patterns("aaaa1234")
assert_true(not r["passed"], "Repeated chars 'aaaa' detected", r["message"])

r = has_repeated_or_sequential_patterns("abc12345")
assert_true(not r["passed"], "Sequential digits '12345' detected", r["message"])

r = has_repeated_or_sequential_patterns("abcdefG1")
assert_true(not r["passed"], "Sequential letters 'abcdef' detected", r["message"])

r = has_repeated_or_sequential_patterns("abcabcG1!")
assert_true(not r["passed"], "Repeated chunk 'abc' detected", r["message"])

r = has_repeated_or_sequential_patterns("qwerty99!")
assert_true(not r["passed"], "Keyboard walk 'qwerty' detected", r["message"])

r = has_repeated_or_sequential_patterns("Tr0ub4dor&7!")
assert_true(r["passed"], "Strong random password has no weak patterns", r["message"])


# ---------------------------------------------------------------------------
# 6. calculate_strength
# ---------------------------------------------------------------------------

section("calculate_strength")

r = calculate_strength("password")
assert_true(r["level"] == "Weak", "'password' is Weak", f"score={r['score']}, level={r['level']}")

r = calculate_strength("Hello2024")
assert_true(r["level"] in ("Medium", "Strong"), "'Hello2024' is Medium or Strong", f"level={r['level']}, score={r['score']}")

r = calculate_strength("Tr0ub4dor&Bicycle#7!")
assert_true(r["level"] == "Strong", "Long complex password is Strong", f"score={r['score']}, level={r['level']}")

r = calculate_strength("johndoe123!", "johndoe")
assert_true(r["score"] < 90, "Password containing username gets penalised", f"score={r['score']}")


# ---------------------------------------------------------------------------
# 7. validate_password -- integration
# ---------------------------------------------------------------------------

section("validate_password -- integration")

r = validate_password("abc")
assert_true(not r["valid"], "3-char password rejected", r["summary"])
assert_true(len(r["errors"]) > 0, "Errors list is non-empty for short password")

r = validate_password("onlylowercase")
assert_true(not r["valid"], "Only-lowercase password rejected", r["summary"])

r = validate_password("password")
assert_true(not r["valid"], "Common password rejected", r["summary"])

r = validate_password("johndoe@2024!", "johndoe")
assert_true(
    not r["valid"] or len(r["warnings"]) > 0,
    "Username in password triggers error or warning",
    r["summary"],
)

r = validate_password("Abcdef12345@", "nobody")
assert_true(
    not r["valid"] or len(r["warnings"]) > 0,
    "Sequential pattern triggers error or warning",
    r["summary"],
)

r = validate_password("Tr0ub4dor&Bicycle#7!", "alice")
assert_true(r["valid"], "Strong password is accepted", r["summary"])
assert_true(r["strength"]["level"] == "Strong", "Strong password scored as Strong")
assert_true(len(r["errors"]) == 0, "No errors for strong password")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

print(f"\n{'=' * 60}")
total = _passed + _failed
print(f"  Results: {_passed}/{total} passed,  {_failed} failed")
print("=" * 60)
if _failed == 0:
    print("  All tests passed.")
else:
    print("  Some tests failed -- check the FAIL lines above.")
