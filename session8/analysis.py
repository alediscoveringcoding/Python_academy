# ============================================================
# FILE 2: analysis.py
# All the business logic lives here
# ============================================================

# --- Thresholds (change these to tune sensitivity) ----------
FUEL_DROP_LIMIT = 10   # litres - big drop while parked = theft
GPS_DEV_LIMIT   = 40   # km     - too far off route
# ------------------------------------------------------------


def build_report(fleet):
    """
    Part 1 - The Accountant
    Goes through every truck and calculates:
    - total distance driven
    - total fuel consumed
    - efficiency score
    Returns a dict with one entry per truck + fleet average.
    """
    report = {}

    for truck in fleet:
        truck_id = truck["id"]
        logs     = truck["logs"]
        plan     = truck["plan"]

        # Add up all distance from every hour
        total_dist = 0
        for log in logs:
            total_dist = total_dist + log["dist_covered"]

        # Fuel used = starting fuel minus final fuel level
        starting_fuel = 400
        final_fuel    = logs[-1]["fuel_level"]
        total_fuel    = starting_fuel - final_fuel

        # Planned fuel = what we expected to burn for this distance
        planned_fuel = (total_dist / 100) * plan["consumption_rate"]

        # Efficiency: planned / actual
        # Score of 1.0 = perfect, below 1.0 = burned more than planned
        if total_fuel > 0:
            efficiency = planned_fuel / total_fuel
        else:
            efficiency = 0

        report[truck_id] = {
            "total_dist": round(total_dist, 1),
            "efficiency": round(efficiency, 2)
        }

    # Fleet average efficiency
    total = 0
    for truck_id in report:
        total = total + report[truck_id]["efficiency"]

    report["FLEET_AVG_EFFICIENCY"] = round(total / len(report), 2)

    return report


def find_suspects(fleet):
    """
    Part 2 - The Detective
    Looks for:
    1. Fuel theft  - big fuel drop while truck is parked
    2. GPS problem - off route for 3+ hours in a row
    Returns a dict of suspicious trucks and why they were flagged.
    """
    suspects = {}

    for truck in fleet:
        truck_id = truck["id"]
        logs     = truck["logs"]

        reasons = []

        # --- Check 1: Fuel Theft ---
        for i in range(1, len(logs)):
            prev_fuel = logs[i - 1]["fuel_level"]
            curr_fuel = logs[i]["fuel_level"]
            fuel_drop = prev_fuel - curr_fuel
            distance  = logs[i]["dist_covered"]

            # Fuel dropped a lot BUT truck barely moved = suspicious
            if fuel_drop > FUEL_DROP_LIMIT and distance < 1.0:
                reasons.append(f"FUEL_THEFT at hour {logs[i]['hour']}")

        # --- Check 2: GPS Route Deviation ---
        bad_hours = 0
        for log in logs:
            if log["gps_deviation"] > GPS_DEV_LIMIT:
                bad_hours = bad_hours + 1
            else:
                bad_hours = 0  # reset counter when back on route

            if bad_hours >= 3:
                reasons.append(f"GPS_DEVIATION for {bad_hours} consecutive hours")
                break  # one flag is enough, stop checking

        # Only add to suspects if we found something
        if reasons:
            suspects[truck_id] = reasons

    return suspects
