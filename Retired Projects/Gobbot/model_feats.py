import math
import json
from collections import defaultdict
from monsters import MONSTER_ENUM, MONSTERCOUNT, MONSTER_ENUM_INV, MONSTER_CR, CONDITION_ENUM_INV
import random
from matplotlib import colormaps

cmap = colormaps['plasma']
bracket_weight = 0.5  # Weight of bracket strength relative to monster strength

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))

def group_cr(cr: int) -> int:
    if cr < -4:
        return -4
    if 3 <= cr <= 4:
        return 3
    if 6 <= cr <= 7:
        return 6
    if 8 <= cr <= 10:
        return 8
    if 11 <= cr <= 13:
        return 11
    if 14 <= cr <= 17:
        return 14
    return cr

class MatchupModel:
    """
    Condition-aware matchup model that handles condition interactions.
    
    Uses:
    - Monster base strength (ELO-like)
    - Condition strength vectors (pre-defined from monsters.py)
    - Condition-condition interaction matrix
    - Condition-monster interaction matrix
    
    Each monster has exactly ONE condition from the pre-defined list.
    """
    
    def __init__(self, trust_threshold=7):
        self.wins = defaultdict(lambda: defaultdict(int))
        self.strength = [0.0] * MONSTERCOUNT
        self.bracket_strength = [0.0] * 20  # For calculating ELO per bracket: from -2 to 17, indexed by +2 offset
        
        # Condition strengths indexed by condition name - pre-initialized from CONDITION_ENUM_INV
        self.condition_strength = {name: 0.0 for name in CONDITION_ENUM_INV.values()}
        
        # Condition-condition interactions: (cond_a, cond_b) -> strength
        self.condition_interactions = defaultdict(float)
        
        # Condition-monster interactions: (condition, monster_idx) -> strength
        self.condition_monster_interactions = defaultdict(float)
        
        self.trust_threshold = trust_threshold

    def _get_condition_strength(self, monster_idx: int, condition: str) -> float:
        """Get effective strength contribution of a condition for a given monster."""
        if not condition or condition not in self.condition_strength:
            return 0.0
        return self.condition_strength[condition] + self.condition_monster_interactions.get((condition, monster_idx), 0.0)

    def _compute_condition_interaction(self, condition_a: str, condition_b: str) -> float:
        """Compute strength modifier from condition-condition interactions."""
        if not condition_a or not condition_b:
            return 0.0
        # Asymmetric: A's condition advantage/disadvantage against B's condition
        key_ab = (condition_a, condition_b)
        key_ba = (condition_b, condition_a)
        return self.condition_interactions.get(key_ab, 0.0) - self.condition_interactions.get(key_ba, 0.0)

    def update(self, winner_idx: int, loser_idx: int, 
               winner_condition: str = "", loser_condition: str = "",
               lr=0.15, condition_lr=0.05, bracket_lr=0.4):
        """
        Update model based on match outcome.
        
        Args:
            winner_idx: Monster index of winner
            loser_idx: Monster index of loser
            winner_condition: Single condition name winner had
            loser_condition: Single condition name loser had
            lr: Learning rate for monster strength
            condition_lr: Learning rate for condition interactions
            bracket_lr: Learning rate for bracket strength
        """
        # Get bracket indices
        winner_bracket = group_cr(MONSTER_CR[MONSTER_ENUM_INV[winner_idx]]) + 2
        loser_bracket = group_cr(MONSTER_CR[MONSTER_ENUM_INV[loser_idx]]) + 2
        
        # Compute predicted win probability with bracket consideration
        strength_diff = self.strength[winner_idx] - self.strength[loser_idx]
        bracket_diff = self.bracket_strength[winner_bracket] - self.bracket_strength[loser_bracket]
        condition_contrib = (self._get_condition_strength(winner_idx, winner_condition) - 
                            self._get_condition_strength(loser_idx, loser_condition))
        interaction_contrib = self._compute_condition_interaction(winner_condition, loser_condition)
        
        combined_diff = strength_diff + bracket_weight * bracket_diff + condition_contrib + interaction_contrib
        p = sigmoid(combined_diff)
        
        # Update monster strength (ELO-like)
        delta = lr * (1 - p)
        self.strength[winner_idx] += delta
        self.strength[loser_idx] -= delta
        
        # Update bracket strength
        bracket_diff = self.bracket_strength[winner_bracket] - self.bracket_strength[loser_bracket]
        p_bracket = sigmoid(bracket_diff)
        delta_bracket = bracket_lr * (1 - p_bracket)
        self.bracket_strength[winner_bracket] += delta_bracket
        self.bracket_strength[loser_bracket] -= delta_bracket
        
        # Update condition strengths based on outcome
        if winner_condition:
            self.condition_strength[winner_condition] += condition_lr * (1 - p)
        if loser_condition:
            self.condition_strength[loser_condition] -= condition_lr * (1 - p)
        
        # Update condition-condition interactions
        if winner_condition and loser_condition:
            key_ab = (winner_condition, loser_condition)
            key_ba = (loser_condition, winner_condition)
            self.condition_interactions[key_ab] += condition_lr * 0.5 * (1 - p)
            self.condition_interactions[key_ba] -= condition_lr * 0.5 * (1 - p)
        
        # Update condition-monster interactions (which conditions help which monsters)
        if winner_condition:
            self.condition_monster_interactions[(winner_condition, winner_idx)] += condition_lr * 0.3 * (1 - p)
            self.condition_monster_interactions[(winner_condition, loser_idx)] -= condition_lr * 0.3 * (1 - p)
        if loser_condition:
            self.condition_monster_interactions[(loser_condition, loser_idx)] += condition_lr * 0.3 * (1 - p)
            self.condition_monster_interactions[(loser_condition, winner_idx)] -= condition_lr * 0.3 * (1 - p)

    def predict(self, a_info: tuple, b_info: tuple, debug: bool = False) -> float:
        """
        Predict win probability for monster A vs monster B.
        
        Args:
            a_info: Tuple of (monster_enum_id, condition_enum_id) for left side
            b_info: Tuple of (monster_enum_id, condition_enum_id) for right side
            debug: Print debug information
            
        Returns:
            Probability that A wins (0.0 to 1.0)
        """
        a, a_condition_id = a_info
        b, b_condition_id = b_info
        
        # Convert condition IDs to names for lookup
        a_condition = CONDITION_ENUM_INV.get(a_condition_id, "") if a_condition_id else ""
        b_condition = CONDITION_ENUM_INV.get(b_condition_id, "") if b_condition_id else ""
        
        # Get bracket indices and bracket strength
        a_name = MONSTER_ENUM_INV[a]
        b_name = MONSTER_ENUM_INV[b]
        a_bracket = group_cr(MONSTER_CR[a_name]) + 2
        b_bracket = group_cr(MONSTER_CR[b_name]) + 2
        
        # Compute strength differential
        strength_diff = self.strength[a] - self.strength[b]
        bracket_diff = self.bracket_strength[a_bracket] - self.bracket_strength[b_bracket]
        
        # Compute condition contributions
        condition_contrib_a = self._get_condition_strength(a, a_condition)
        condition_contrib_b = self._get_condition_strength(b, b_condition)
        condition_contrib = condition_contrib_a - condition_contrib_b
        
        # Compute condition-condition interactions
        interaction_contrib = self._compute_condition_interaction(a_condition, b_condition)
        
        # Compute final prediction from model
        total_diff = strength_diff + bracket_weight * bracket_diff + condition_contrib + interaction_contrib
        p = sigmoid(total_diff)
        
        if debug:
            # Direct matchup history for reference
            w_ab = self.wins[a][b]
            w_ba = self.wins[b][a]
            total = w_ab + w_ba
            
            if total > 0:
                p_direct = w_ab / total
                print(f"Direct matches: {w_ab} vs {w_ba} ({p_direct:.2f})")
            else:
                print(f"No direct match history")
            
            print(f"Model prediction breakdown:")
            print(f"  Monster strength: {strength_diff:.2f}")
            print(f"  Bracket strength: {bracket_weight * bracket_diff:.2f}")
            print(f"  Condition contribution: {condition_contrib:.2f}")
            print(f"  Condition interactions: {interaction_contrib:.2f}")
            print(f"  Final prediction: {p:.2f}")
            
            if a_condition:
                print(f"Left condition: {a_condition}")
            if b_condition:
                print(f"Right condition: {b_condition}")
        
        return p

    def print_model(self):
        """Generate HTML heatmap of matchups (ignoring conditions for overview)."""
        winprobs = [[0.0]*MONSTERCOUNT for _ in range(MONSTERCOUNT)]
        sortedmonsters = sorted(range(MONSTERCOUNT), key=lambda x: self.strength[x], reverse=True)
        
        for i in range(MONSTERCOUNT):
            for j in range(MONSTERCOUNT):
                a = sortedmonsters[i]
                b = sortedmonsters[j]
                winprobs[i][j] = self.predict((a, None), (b, None), debug=False)
        
        # Create heatmap
        heatmap = []
        for i in range(MONSTERCOUNT):
            row = []
            for j in range(MONSTERCOUNT):
                p = winprobs[i][j]
                color = cmap(p)
                r, g, b = int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
                row.append(f"rgb({r},{g},{b})")
            heatmap.append(row)

        # Save to HTML
        table_width = 100 * (MONSTERCOUNT + 1)
        with open("matchup_heatmap_conditions.html", "w", encoding="utf-8") as f:
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
                f.write(f"<tr><th>{monster_name} (Strength: {strength:.2f})</th>")
                for j in range(MONSTERCOUNT):
                    color = heatmap[i][j]
                    f.write(f"<td style='background-color:{color};'></td>")
                f.write("</tr>\n")
            
            f.write("</table></body></html>\n")
        
        print(f"Generated heatmap with {len(self.condition_strength)} conditions tracked")

def train_from_log(
    model: MatchupModel,
    path="training_log.jsonl",
    passes=5,
    base_lr=0.13
):
    """
    Train the model from a JSONL log of matches.
    
    Log format: {"left_monster": str, "right_monster": str, "left_condition": str, 
                 "right_condition": str, "winner": "LEFT"|"RIGHT"}
    
    Each monster has exactly one condition from the pre-defined list in monsters.py.
    """
    matches = []

    # Load matches
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)

            left = MONSTER_ENUM[row["left_monster"]]
            right = MONSTER_ENUM[row["right_monster"]]

            # Skip matches with Starts Invisible (too dominant)
            if row.get("left_condition") == "Starts Invisible" or row.get("right_condition") == "Starts Invisible":
                continue

            left_condition = row.get("left_condition", "")
            right_condition = row.get("right_condition", "")

            if row["winner"] == "LEFT":
                winner, loser = left, right
                winner_condition, loser_condition = left_condition, right_condition
            else:
                winner, loser = right, left
                winner_condition, loser_condition = right_condition, left_condition

            # Empirical evidence (ONCE)
            model.wins[winner][loser] += 1

            # Store for training
            matches.append((winner, loser, winner_condition, loser_condition))

    # Multi-pass training
    for i in range(passes):
        lr = base_lr / (i + 1)
        condition_lr = 0.05 / (i + 1)
        random.shuffle(matches)

        for winner, loser, winner_condition, loser_condition in matches:
            model.update(winner, loser, winner_condition, loser_condition, lr=lr, condition_lr=condition_lr)

    model.print_model()
    print(f"\nModel training complete.")
    print(f"  Monsters: {MONSTERCOUNT}")
    print(f"  Conditions: {len(model.condition_strength)}")
    print(f"  Total condition-condition interactions: {len(model.condition_interactions)}")
    print(f"  Total condition-monster interactions: {len(model.condition_monster_interactions)}")
