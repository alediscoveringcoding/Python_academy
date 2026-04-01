# ============================================================
# FILE 4: test_analysis.py
# Unit tests - uses fake/stub data, NOT the real fleet file
# Run with: python test_analysis.py
# ============================================================

from analysis import build_report, find_suspects


# ============================================================
# STUB DATA HELPERS
# We build tiny fake trucks instead of loading the real file
# ============================================================

def make_log(hour, fuel, dist, gps=5.0):
    """ Creates one fake hourly log entry """
    return {
        "hour":          hour,
        "fuel_level":    fuel,
        "dist_covered":  dist,
        "gps_deviation": gps,
        "road_block":    False
    }

def make_truck(truck_id, logs):
    """ Creates one fake truck with the given logs """
    return {
        "id":   truck_id,
        "plan": {"dist_km": 2500, "eta_hrs": 120, "consumption_rate": 16},
        "logs": logs
    }


# ============================================================
# TEST HELPERS - simple pass/fail printer
# ============================================================

passed = 0
failed = 0

def check(label, condition):
    global passed, failed
    if condition:
        print(f"  PASS  {label}")
        passed += 1
    else:
        print(f"  FAIL  {label}")
        failed += 1


# ============================================================
# TESTS: build_report
# ============================================================

print("\n[ build_report tests ]")

# Build a simple 2-hour truck
logs = [
    make_log(0, fuel=400, dist=20),
    make_log(1, fuel=396, dist=20),
]
fleet  = [make_truck("TRUCK-1", logs)]
report = build_report(fleet)

check("truck appears in report",           "TRUCK-1" in report)
check("fleet average key exists",          "FLEET_AVG_EFFICIENCY" in report)
check("total_dist is positive",            report["TRUCK-1"]["total_dist"] > 0)
check("efficiency is positive",            report["TRUCK-1"]["efficiency"] > 0)
check("single truck: avg == efficiency",   report["FLEET_AVG_EFFICIENCY"] == report["TRUCK-1"]["efficiency"])


# ============================================================
# TESTS: find_suspects - fuel theft
# ============================================================

print("\n[ fuel theft tests ]")

# Normal driving - no theft
logs = [
    make_log(0, fuel=400, dist=20),
    make_log(1, fuel=396, dist=20),  # small drop while moving = normal
]
suspects = find_suspects([make_truck("TRUCK-CLEAN", logs)])
check("clean truck not flagged",           "TRUCK-CLEAN" not in suspects)

# Big drop while parked = theft
logs = [
    make_log(0, fuel=400, dist=20),
    make_log(1, fuel=340, dist=0.0),  # 60 litre drop, not moving!
]
suspects = find_suspects([make_truck("TRUCK-THIEF", logs)])
check("theft detected when parked",        "TRUCK-THIEF" in suspects)

# Big drop but truck is moving = not theft, just a hungry engine
logs = [
    make_log(0, fuel=400, dist=20),
    make_log(1, fuel=340, dist=25),  # big drop but driving fast
]
suspects = find_suspects([make_truck("TRUCK-OK", logs)])
check("no theft when truck is moving",     "TRUCK-OK" not in suspects)

# Small drop while parked = not theft (below limit)
logs = [
    make_log(0, fuel=400, dist=20),
    make_log(1, fuel=395, dist=0.0),  # only 5 litres, under limit
]
suspects = find_suspects([make_truck("TRUCK-FINE", logs)])
check("small drop while parked = ignored", "TRUCK-FINE" not in suspects)


# ============================================================
# TESTS: find_suspects - GPS deviation
# ============================================================

print("\n[ GPS deviation tests ]")

# 3 hours in a row off route = flagged
logs = [make_log(h, fuel=400 - h, dist=20, gps=55.0) for h in range(5)]
suspects = find_suspects([make_truck("TRUCK-LOST", logs)])
check("GPS deviation flagged after 3hrs",  "TRUCK-LOST" in suspects)

# Only 2 bad hours = not flagged
logs = [
    make_log(0, fuel=400, dist=20, gps=55.0),
    make_log(1, fuel=399, dist=20, gps=55.0),
    make_log(2, fuel=398, dist=20, gps=5.0),  # back on route
]
suspects = find_suspects([make_truck("TRUCK-WANDERED", logs)])
check("2 bad GPS hours = not flagged",     "TRUCK-WANDERED" not in suspects)

# Good GPS all week = not flagged
logs = [make_log(h, fuel=400 - h, dist=20, gps=10.0) for h in range(10)]
suspects = find_suspects([make_truck("TRUCK-GOOD-GPS", logs)])
check("clean GPS = not flagged",           "TRUCK-GOOD-GPS" not in suspects)


# ============================================================
# RESULTS
# ============================================================

print("\n" + "=" * 40)
print(f"  {passed} passed,  {failed} failed")
print("=" * 40 + "\n")
