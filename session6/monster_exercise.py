import json

# def total_score_of_monster(monster: dict) -> float:
#     return sum(monster["scores"])

# def avg_round_score_of_monster(monster: dict) -> float:
#     return total_score_of_monster(monster) / len(monster["scores"])

def total_score(monsterScore: list) -> float:
    return sum(monsterScore)

def avg_round_score(monsterScore: list) -> float:
    return total_score(monsterScore) / len(monsterScore)

def best_round(monsterScore: list) -> float:
    return max(monsterScore)

def worst_round(monsterScore: list) -> float:
    return min(monsterScore)

def assign_rank_label(totalScore: float) -> str:
    if totalScore >= 40:
        return "Legend"
    elif totalScore >= 25:
        return "Elite"
    elif totalScore >= 10:
        return "Fighter"
    elif totalScore >= 0:
        return "Rookie"
    else:
        return "Fallen"

def get_stability(monsterScore: list) -> str:
    return "Stable" if worst_round(monsterScore) >= 0 else "Unstable"

def get_monsters_by_element(monsterSummaries: list, element: str) -> list:
    return [monster for monster in monsterSummaries if monster["element"] == element]

def get_monsters_by_rank(monsterSummaries: list, rank: str) -> list:
    return [monster for monster in monsterSummaries if monster["rank"] == rank]

def get_monsters_by_best_round(monsterSummaries: list, bestRound: float) -> list:
    return [monster for monster in monsterSummaries if monster["best"] is not None and monster["best"] >= bestRound]

def get_monster_summaries(monsters: list) -> list:
    monster_summaries = []

    for monster in monsters:
        monster_summaries.append({
            "name": monster["name"],
            "element": monster["element"],
            "total": 0 if len(monster["scores"]) == 0 else total_score(monster["scores"]),
            "average": 0 if len(monster["scores"]) == 0 else avg_round_score(monster["scores"]),
            "best": None if len(monster["scores"]) == 0 else best_round(monster["scores"]),
            "worst": None if len(monster["scores"]) == 0 else worst_round(monster["scores"]),
            "rank": assign_rank_label(total_score(monster["scores"])),
            "stability": None if len(monster["scores"]) == 0 else get_stability(monster["scores"])
        })

    return monster_summaries

def final_report(monsterSummaries: list):
    print("=" * 60)
    print("MONSTER TOURNAMENT FINAL REPORT")
    print("=" * 60)
    
    print("\nMONSTER SUMMARIES")
    print("-" * 40)
    for i, monster in enumerate(monsterSummaries, 1):
        print(f"{i}. {monster['name']} ({monster['element']})")
        print(f"   Total Score: {monster['total']} | Average: {monster['average']:.2f}")
        print(f"   Best Round: {monster['best']} | Worst Round: {monster['worst']}")
        print(f"   Rank: {monster['rank']} | Stability: {monster['stability']}")
        print()
    
    print("\nFINAL STATISTICS")
    print("-" * 40)
    print(f"Total number of monsters: {len(monsterSummaries)}")
    
    allAverages = []
    for monster in monsterSummaries:
        allAverages.append(monster["average"])
    print(f"Average tournament score: {avg_round_score(allAverages):.2f}")
    
    highest = max(monsterSummaries, key=lambda x: x['total'])
    print(f"Highest scoring monster: {highest['name']} ({highest['total']} points)")
    
    lowest = min(monsterSummaries, key=lambda x: x['total'] if x['total'] != 0 else float('inf'))
    print(f"Lowest scoring monster: {lowest['name']} ({lowest['total']} points)")
    
    rankDict = {}
    for monster in monsterSummaries:
        if monster["rank"] not in rankDict:
            rankDict[monster["rank"]] = []
        rankDict[monster["rank"]].append(monster)

    print("\nMONSTERS BY RANK")
    print("-" * 40)
    for rank in rankDict:
        rankMonsters = get_monsters_by_rank(monsterSummaries, rank)
        print(f"Rank: {rank} ({len(rankMonsters)} monsters)")
        for monster in rankMonsters:
            print(f"  - {monster['name']}: {monster['total']} points")
        print()
    
    stable_count = len([m for m in monsterSummaries if m['stability'] == 'Stable'])
    unstable_count = len([m for m in monsterSummaries if m['stability'] == 'Unstable'])
    print("STABILITY ANALYSIS")
    print("-" * 40)
    print(f"Stable monsters: {stable_count}")
    print(f"Unstable monsters: {unstable_count}")
    
    chosenElement = input("\nChoose an element to search monsters by: ")
    element_monsters = get_monsters_by_element(monsterSummaries, chosenElement)
    print(f"\nMonsters with {chosenElement} element ({len(element_monsters)} found):")
    if element_monsters:
        for monster in element_monsters:
            print(f"  - {monster['name']}: {monster['total']} points")
    else:
        print("  No monsters found with this element.")
    
    bestRoundMonsters = get_monsters_by_best_round(monsterSummaries, 20)
    print(f"\nMonsters with best round score of at least 20 ({len(bestRoundMonsters)} found):")
    if bestRoundMonsters:
        for monster in bestRoundMonsters:
            print(f"  - {monster['name']}: Best round = {monster['best']}")
    else:
        print("  No monsters achieved a round score of 20 or higher.")
    
    print("\n" + "=" * 60)
    print("TOURNAMENT ANALYSIS COMPLETE")
    print("=" * 60)

def main():
    # monsters = [
    #     {"name": "Pyrofang", "scores": [12, 18, -5, 20], "element": "fire"},
    #     {"name": "Aquanox", "scores": [10, 0, 8, 15], "element": "water"},
    #     {"name": "Stoneclaw", "scores": [25, -10, 5], "element": "earth"},
    #     {"name": "Zephyra", "scores": [9, 14, 11, 13, 10], "element": "air"},
    #     {"name": "Shadowbite", "scores": [], "element": "dark"},
    #     {"name": "Voltaris", "scores": [30, -20, 25, -5], "element": "lightning"}
    # ]

    with open("monsters.json", "r") as f:
        monsters = json.load(f)

    monsterSummaries = get_monster_summaries(monsters)
    final_report(monsterSummaries)

if __name__ == "__main__":
    main()