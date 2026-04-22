# ============================================================
# FILE 1: generate_data.py
# Run this FIRST - creates fleet_data.json
# ============================================================

import random
import json

def generate_data():
    fleet = []

    for t_id in range(100, 150):

        truck = {
            "id": f"TRUCK-{t_id}",
            "plan": {"dist_km": 2500, "eta_hrs": 120, "consumption_rate": 16},
            "logs": []
        }

        fuel = 400

        for h in range(168):
            dist_moved = random.uniform(15, 25)
            fuel_loss = (dist_moved / 100) * truck["plan"]["consumption_rate"]

            if t_id == 105 and h == 20:
                fuel -= 50  # Theft event

            fuel -= fuel_loss

            truck["logs"].append({
                "hour": h,
                "gps_deviation": random.uniform(0, 15) if t_id != 110 else random.uniform(0, 60),
                "fuel_level": round(fuel, 2),
                "dist_covered": round(dist_moved, 2),
                "road_block": random.choice([True, False]) if random.random() > 0.95 else False
            })

        fleet.append(truck)

    return fleet


# Run and save to JSON
fleet_data = generate_data()

with open("fleet_data.json", "w") as f:
    json.dump(fleet_data, f)

print("Done! Created fleet_data.json with", len(fleet_data), "trucks.")
