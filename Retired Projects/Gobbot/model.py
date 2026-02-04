import math
import json
from collections import defaultdict
from monsters import MONSTER_ENUM, MONSTERCOUNT, MONSTER_ENUM_INV, MONSTER_CR
import random
from matplotlib import colormaps

cmap = colormaps['plasma']
bracket_weight = 1.0

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))

def group_cr(cr: int) -> int:
    if cr < -4:
        return -4
    # if 0 <= cr <= 1: # 1, 0
    #     return 0
    if 3 <= cr <= 4: # 4, 3
        return 3
    if 6 <= cr <= 7: # 7, 6
        return 6
    if 8 <= cr <= 10: # 10, 9, 8
        return 8
    if 11 <= cr <= 13: # 13, 12, 11 CONFIRMED EXISTS
        return 11
    if 14 <= cr <= 17: # 17, 16, 15, 14
        return 14
    return cr

class MatchupModel:
    def __init__(self, trust_threshold=7):
        self.wins = defaultdict(lambda: defaultdict(int))
        self.strength = [0.0] * MONSTERCOUNT
        self.bracket_strength = [0.0] * 20 # For calculating ELO per bracket. from -2 to 17 so 20 brackets.
        self.trust_threshold = trust_threshold

    def update(self, winner: int, loser: int, lr=0.15, bracket_lr=0.2):
        # Get bracket indices first (needed for both updates)
        winner_bracket = group_cr(MONSTER_CR[MONSTER_ENUM_INV[winner]]) + 2
        loser_bracket = group_cr(MONSTER_CR[MONSTER_ENUM_INV[loser]]) + 2
        
        # Update global strength with bracket consideration
        strength_diff = self.strength[winner] - self.strength[loser]
        bracket_diff = self.bracket_strength[winner_bracket] - self.bracket_strength[loser_bracket]
        combined_diff = strength_diff + bracket_weight * bracket_diff
        p = sigmoid(combined_diff)
        # # Update global strength only (Elo-like)
        # diff = self.strength[winner] - self.strength[loser]
        # p = sigmoid(diff)

        delta = lr * (1 - p)
        self.strength[winner] += delta
        self.strength[loser] -= delta

        # Update bracket strength
        winner_bracket = group_cr(MONSTER_CR[MONSTER_ENUM_INV[winner]]) + 2
        loser_bracket = group_cr(MONSTER_CR[MONSTER_ENUM_INV[loser]]) + 2
        bracket_diff = self.bracket_strength[winner_bracket] - self.bracket_strength[loser_bracket]
        p_bracket = sigmoid(bracket_diff)
        delta_bracket = bracket_lr * (1 - p_bracket)
        self.bracket_strength[winner_bracket] += delta_bracket
        self.bracket_strength[loser_bracket] -= delta_bracket

    def predict(self, a: int, b: int, debug: bool) -> float:
        w_ab = self.wins[a][b]
        w_ba = self.wins[b][a]
        total = w_ab + w_ba

        # Transitive estimate
        strength_diff = self.strength[a] - self.strength[b]
        p_trans = sigmoid(strength_diff)

        # Bracket adjustment
        a_bracket = group_cr(MONSTER_CR[MONSTER_ENUM_INV[a]]) + 2
        b_bracket = group_cr(MONSTER_CR[MONSTER_ENUM_INV[b]]) + 2
        cum_strength_a = self.strength[a] + self.bracket_strength[a_bracket] * bracket_weight
        cum_strength_b = self.strength[b] + self.bracket_strength[b_bracket] * bracket_weight
        bracket_diff = cum_strength_a - cum_strength_b
        p_bracket_included = sigmoid(bracket_diff)

        print(f"Elo of Left: {self.strength[a]:.2f}\nElo of Right: {self.strength[b]:.2f}\nTransitive win probability: {p_trans:.2f}") if debug else None
        print(f"Bracket adjusted Elo of Left: {cum_strength_a:.2f}\nBracket adjusted Elo of Right: {cum_strength_b:.2f}\nBracket adjusted win probability: {p_bracket_included:.2f}") if debug and a_bracket != b_bracket else None

        if total == 0:
            print("No direct matches, relying entirely on transitive estimate") if debug else None
            return p_bracket_included

        p_direct = w_ab / total
        print(f"Left's direct win rate over Right: {p_direct:.2f} based on {total} matches") if debug else None
        alpha = min(1.0, total / self.trust_threshold)

        prediction = alpha * p_direct + (1 - alpha) * p_bracket_included
        print(f"Using alpha={alpha:.2f}, final prediction: {max(prediction, 1-prediction):.2f} for {MONSTER_ENUM_INV[a] if prediction > 0.5 else MONSTER_ENUM_INV[b]}") if debug else None

        return prediction
    
    def print_model(self):
        # Make a Matrix of predicted win probabilities, sorted by ELO
        winprobs = [[0.0]*MONSTERCOUNT for _ in range(MONSTERCOUNT)]
        sortedmonsters = sorted(range(MONSTERCOUNT), key=lambda x: (group_cr(MONSTER_CR[MONSTER_ENUM_INV[x]]), self.strength[x]), reverse=True)
        for i in range(MONSTERCOUNT):
            for j in range(MONSTERCOUNT):
                a = sortedmonsters[i]
                b = sortedmonsters[j]
                winprobs[i][j] = self.predict(a, b, debug=False)
        
        # Turn this matrix into a list of colors to be used as a heatmap
        heatmap = []
        for i in range(MONSTERCOUNT):
            row = []
            for j in range(MONSTERCOUNT):
                p = winprobs[i][j]
                color = cmap(p)
                r, g, b = int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
                row.append(f"rgb({r},{g},{b})")
            heatmap.append(row)

        # save to html with each matchup being a square of the appropriate color
        table_width = 100 * (MONSTERCOUNT + 1)
        with open("matchup_heatmap.html", "w", encoding="utf-8") as f:
            f.write(f"<html><head><style>table {{ table-layout: fixed; border-collapse: collapse; width: {table_width}px; }} td, th {{ width: 100px; height: 100px; border: 0px solid #000; }}</style></head><body><table>\n")
            # Header row
            f.write("<tr><th></th>")
            for j in range(MONSTERCOUNT):
                monster_name = MONSTER_ENUM_INV[sortedmonsters[j]]
                f.write(f"<th><div style='width: 100px; transform: rotate(-90deg);'>{monster_name}</div></th>")
            f.write("</tr>\n")

            for i in range(MONSTERCOUNT):
                monster_name = MONSTER_ENUM_INV[sortedmonsters[i]]
                strength = self.strength[sortedmonsters[i]]
                bracket_strength = self.bracket_strength[group_cr(MONSTER_CR[monster_name]) + 2]
                f.write(f"<tr><th>{monster_name} (ELO: {strength + bracket_strength * bracket_weight:.2f})</th>")
                for j in range(MONSTERCOUNT):
                    color = heatmap[i][j]
                    f.write(f"<td style='background-color:{color};'></td>")
                f.write("</tr>\n")
            f.write("</table></body></html>\n")

    def print_model_no_brackets(self):
        # Make a Matrix of predicted win probabilities, sorted by ELO
        winprobs = [[0.0]*MONSTERCOUNT for _ in range(MONSTERCOUNT)]
        bracket_strengths = []
        for i in range(MONSTERCOUNT):
            monster_name = MONSTER_ENUM_INV[i]
            bracket_strengths.append(self.bracket_strength[group_cr(MONSTER_CR[monster_name]) + 2] * bracket_weight)
        sortedmonsters = sorted(range(MONSTERCOUNT), key=lambda x: self.strength[x] + bracket_strengths[x], reverse=True)
        for i in range(MONSTERCOUNT):
            for j in range(MONSTERCOUNT):
                a = sortedmonsters[i]
                b = sortedmonsters[j]
                winprobs[i][j] = self.predict(a, b, debug=False)
        
        # Turn this matrix into a list of colors to be used as a heatmap
        heatmap = []
        for i in range(MONSTERCOUNT):
            row = []
            for j in range(MONSTERCOUNT):
                p = winprobs[i][j]
                color = cmap(p)
                r, g, b = int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
                row.append(f"rgb({r},{g},{b})")
            heatmap.append(row)

        # save to html with each matchup being a square of the appropriate color
        table_width = 100 * (MONSTERCOUNT + 1)
        with open("matchup_heatmap_bracketless.html", "w", encoding="utf-8") as f:
            f.write(f"<html><head><style>table {{ table-layout: fixed; border-collapse: collapse; width: {table_width}px; }} td, th {{ width: 100px; height: 100px; border: 0px solid #000; }}</style></head><body><table>\n")
            # Header row
            f.write("<tr><th></th>")
            for j in range(MONSTERCOUNT):
                monster_name = MONSTER_ENUM_INV[sortedmonsters[j]]
                f.write(f"<th><div style='width: 100px; transform: rotate(-90deg);'>{monster_name}</div></th>")
            f.write("</tr>\n")

            for i in range(MONSTERCOUNT):
                monster_name = MONSTER_ENUM_INV[sortedmonsters[i]]
                strength = self.strength[sortedmonsters[i]]
                bracket_strength = self.bracket_strength[group_cr(MONSTER_CR[monster_name]) + 2]
                f.write(f"<tr><th>{monster_name} (ELO: {strength + bracket_strength:.2f})</th>")
                for j in range(MONSTERCOUNT):
                    color = heatmap[i][j]
                    f.write(f"<td style='background-color:{color};'></td>")
                f.write("</tr>\n")
            f.write("</table></body></html>\n")

def train_from_log(
    model: MatchupModel,
    path="training_log.jsonl",
    passes=5,
    base_lr=0.13
):
    matches = []

    # Load once, count empirical evidence once
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)

            left = MONSTER_ENUM[row["left_monster"]]
            right = MONSTER_ENUM[row["right_monster"]]

            # Skip if either monster starts invisible, that feat is just so strong that it fucks with everything
            if row.get("left_condition") == "Starts Invisible" or row.get("right_condition") == "Starts Invisible":
                continue

            if row["winner"] == "LEFT":
                winner, loser = left, right
            else:
                winner, loser = right, left

            # Empirical evidence (ONCE)
            model.wins[winner][loser] += 1

            # Store for strength training
            matches.append((winner, loser))

    # Multi-pass shuffled strength training
    for i in range(passes):
        lr = base_lr / (i + 1)
        # random.shuffle(matches)

        for winner, loser in matches:
            model.update(winner, loser, lr=lr)

    model.print_model()
    model.print_model_no_brackets()
