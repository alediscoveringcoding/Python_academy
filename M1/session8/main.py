# ============================================================
# FILE 3: main.py
# Run this SECOND - loads fleet_data.json and prints results
# ============================================================

import json
from analysis import build_report, find_suspects


# --- Load the data ------------------------------------------
with open("fleet_data.json") as f:
    fleet_data = json.load(f)


# --- Run the analysis ---------------------------------------
report   = build_report(fleet_data)
suspects = find_suspects(fleet_data)


# --- Combine into one final dictionary ----------------------
final_output = {
    "report":    report,
    "anomalies": suspects
}


# --- Pretty print (JSON style) ------------------------------
print(json.dumps(final_output, indent=2))


# --- Quick summary at the bottom ----------------------------
print("\n" + "=" * 50)
print("  Trucks checked :", len(fleet_data))
print("  Fleet avg eff.  :", report["FLEET_AVG_EFFICIENCY"])
print("  Suspects found  :", len(suspects))
print("-" * 50)
for truck_id in suspects:
    for reason in suspects[truck_id]:
        print(f"  ⚠  {truck_id} → {reason}")
print("=" * 50)
