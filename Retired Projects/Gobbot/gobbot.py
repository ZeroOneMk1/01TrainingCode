from GobDat.consts import *
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from math import sqrt, log, floor
import traceback
from matplotlib import pyplot as plt

import random as rd
import re

from time import sleep



def wait_for_bets_score_not_zero(driver, timeout=10):
    """Waits until an element with class 'BetsScore' has non-zero text."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda driver: driver.find_element(By.CLASS_NAME, "BetsScore").text != "0"
        )
        return True  # Element found and has non-zero text
    except TimeoutException:
        print("Timeout: BetsScore element did not become non-zero within the specified time.")
        return False # element was not found, or text was never non-zero

def parse(page: str) -> None:
    return None


def betting() -> bool:
    return browser.find_element("xpath", BETTINGBANNER).text == "PLACE YOUR BET"


def is_caps(string: str) -> bool:
    for char in string:
        if ord(char) < ord('A') or ord(char) > ord('Z'):
            return False
    return True

def chat(msg: str):
    browser.find_element("class name", "ChatInput").send_keys(msg)
    browser.find_element("class name", "SendButton").click()

def parse_attacks(side: str, stats: dict) -> dict:
    stats[side]["ACTIONS_PARSED"] = {}
    for action in stats[side]["ACTIONS"]:
        try:
            action = re.sub(r" \(If[^\)]+\)", "", action)
            name = re.findall(r"([\w\ \(\)]+):", action)[0]
        except:
            print(f"FAILED TO PARSE ACTION NAME: {action}")
            continue
        if "Multi" not in name:
            stats[side]["ACTIONS_PARSED"][name] = {"HIT": 0, "NUMBER_DIE": [], "DMG_DIE": [], "FLAT": 0, "TYPE": ["None"], "RANGE": 0, "SAVE": "None", "DAMAGE": 0}
            try:
                stats[side]["ACTIONS_PARSED"][name]["HIT"] = int(re.findall(r"(\d+),", action)[0])
            except:
                stats[side]["ACTIONS_PARSED"][name]["HIT"] = 0
            try:
                stats[side]["ACTIONS_PARSED"][name]["NUMBER_DIE"] = re.findall(r"(\d+)d\d+", action)
                stats[side]["ACTIONS_PARSED"][name]["DMG_DIE"] = re.findall(r"\d+d(\d+)", action)
                stats[side]["ACTIONS_PARSED"][name]["TYPE"] = re.findall(r"Piercing|Slashing|Bludgeoning|Necrotic|Radiant|Cold|Fire|Thunder|Psychic|Lightning|Force|Acid|Poison", action)
            except Exception as e:
                print(f"FAILED AROUND LIKE 44-56: {e}")
            
            try:
                stats[side]["ACTIONS_PARSED"][name]["FLAT"] = int(re.findall(r"\d+d\d+\+(\d+)", action)[0])
            except:
                stats[side]["ACTIONS_PARSED"][name]["FLAT"] = 0
            try:
                stats[side]["ACTIONS_PARSED"][name]["RANGE"] = int(re.findall(r"(\d+)ft", action)[0])
            except:
                stats[side]["ACTIONS_PARSED"][name]["RANGE"] = 5
            try:
                stats[side]["ACTIONS_PARSED"][name]["SAVE"] = re.findall(r"(\w+) Save", action)[0]
            except:
                stats[side]["ACTIONS_PARSED"][name]["SAVE"] = "None"
        else:
            action = re.findall(r": ([^\n]+)", action)[0]
            stats[side]["ACTIONS_PARSED"][name] = {"RANGE": 0, "ACTIONS": 0}
            try:
                stats[side]["ACTIONS_PARSED"][name]["RANGE"] = int(re.findall(r"(\d+)ft, ", action)[0])
            except:
                stats[side]["ACTIONS_PARSED"][name]["RANGE"] = 5
            try:
                action = re.findall(r"\d+ft, ([\w\W]+)", action)[0]
            except:
                print("Couldn't remove range from multiattack.")
            # turn 2x (Bite, Claw) into '2 Bite, 2 Claw'
            action = re.sub(r'(\d+)x \(([\w\W]+?)\)', lambda m: ', '.join([f"{m.group(1)} {attack.strip()}" for attack in m.group(2).split(',')]), action)

            stats[side]["ACTIONS_PARSED"][name]["ACTIONS"] = action.split(", ")
    return stats

def determine_dpr(side: str, stats: dict) -> dict:

    if side == "LEFT":
        other = "RIGHT"
    else:
        other = "LEFT"

    for action in stats[side]["ACTIONS_PARSED"]:
        if "Multi" not in action:
            
            for i in range(len(stats[side]["ACTIONS_PARSED"][action]["NUMBER_DIE"])):
                if i == 0:
                    dmg = int(stats[side]["ACTIONS_PARSED"][action]["NUMBER_DIE"][i]) * (int(stats[side]["ACTIONS_PARSED"][action]["DMG_DIE"][i]) + 1)/2 + int(stats[side]["ACTIONS_PARSED"][action]["FLAT"])
                else:
                    dmg = int(stats[side]["ACTIONS_PARSED"][action]["NUMBER_DIE"][i]) * (int(stats[side]["ACTIONS_PARSED"][action]["DMG_DIE"][i]) + 1)/2

                try:
                    if stats[side]["ACTIONS_PARSED"][action]["TYPE"][i] in stats[other]["VULNERABLE"]:
                        dmg *= 2
                    elif stats[side]["ACTIONS_PARSED"][action]["TYPE"][i] in stats[other]["RESIST"]:
                        dmg /= 2
                    elif stats[side]["ACTIONS_PARSED"][action]["TYPE"][i] in stats[other]["IMMUNE"] or stats[side]["ACTIONS_PARSED"][action]["TYPE"][i] in stats[other]["ABSORB"]:
                        dmg = 0
                except Exception as e:
                    print(f"FAILED TO APPLY ATTACK DAMAGE TYPE: {e}")
                    print(stats[side]["ACTIONS_PARSED"][action]["TYPE"])
                
                stats[side]["ACTIONS_PARSED"][action]["DAMAGE"] += dmg

    for action in stats[side]["ACTIONS_PARSED"]:
        if "Multi" in action:
            print(f"Calculating multiattack damage for {stats[side]["ACTIONS_PARSED"][action]["ACTIONS"]}")
            dmg = 0
            for attack in stats[side]["ACTIONS_PARSED"][action]["ACTIONS"]:
                try:
                    multiplier = int(re.findall(r"(\d+)", attack)[0])
                    dmg += multiplier * stats[side]["ACTIONS_PARSED"][attack[2+floor(log(multiplier, 10)):]]["DAMAGE"]
                except:
                    multiplier = 1
                    dmg += multiplier * stats[side]["ACTIONS_PARSED"][attack]["DAMAGE"]

            stats[side]["ACTIONS_PARSED"][action]["DAMAGE"] = dmg
    
    high = 1
    for action in stats[side]["ACTIONS_PARSED"]:
        if stats[side]["ACTIONS_PARSED"][action]["DAMAGE"] > high:
            high = stats[side]["ACTIONS_PARSED"][action]["DAMAGE"]
    stats[side]["DPR"] = high

    return stats

def check_PC(stats) -> bool:
    """Checks if either combatant is a PC by looking for the 'PC Class' tag in Conditions."""
    left_conditions = stats["LEFT"]["CONDITIONS"]
    right_conditions = stats["RIGHT"]["CONDITIONS"]
    if "PC Class" in left_conditions or "PC Class" in right_conditions:
        return True
    return False

def login() -> None:

    browser.get(LOGINURL)

    sleep(4)

    browser.find_element("xpath", LOGINLOCATION).click()

    browser.find_element("xpath", USERNAMEBUTTON).send_keys(EMAIL)
    browser.find_element("xpath", PASSWORDBUTTON).send_keys(PASS)

    browser.find_element("xpath", LOGINBUTTON).click()

    sleep(4)
    
    try:
        browser.find_element("xpath", CONTINUEBUTTON).click()
    except:
        browser.find_element("xpath", CONTINUEBUTTON_ASCENT).click()

def login_two() -> None:

    for browsertwo, i in zip(counterbetters, range(counterbettercount)):
        browsertwo.get(LOGINURL)

        sleep(4)

        browsertwo.find_element("xpath", LOGINLOCATION).click()

        browsertwo.find_element("xpath", USERNAMEBUTTON).send_keys(COUNTEREMAILS[i])
        browsertwo.find_element("xpath", PASSWORDBUTTON).send_keys(COUNTERPASSES[i])

        browsertwo.find_element("xpath", LOGINBUTTON).click()

        sleep(4)

        browsertwo.find_element("xpath", CONTINUEBUTTON).click()


def get_stats(right, left) -> dict:

    stats = {}

    stats["RIGHT"] = {}
    stats["RIGHT"]["NAME"] = right

    stats["LEFT"] = {}
    stats["LEFT"]["NAME"] = left

    #*____________LEFTSIDE_____________

    stats["LEFT"]["STR"] = int(re.findall(r"\d+", browser.find_element("xpath", LEFTSIDE_STR).text)[0])
    stats["LEFT"]["DEX"] = int(re.findall(r"\d+", browser.find_element("xpath", LEFTSIDE_DEX).text)[0])
    stats["LEFT"]["CON"] = int(re.findall(r"\d+", browser.find_element("xpath", LEFTSIDE_CON).text)[0])
    stats["LEFT"]["INT"] = int(re.findall(r"\d+", browser.find_element("xpath", LEFTSIDE_INT).text)[0])
    stats["LEFT"]["WIS"] = int(re.findall(r"\d+", browser.find_element("xpath", LEFTSIDE_WIS).text)[0])
    stats["LEFT"]["CHA"] = int(re.findall(r"\d+", browser.find_element("xpath", LEFTSIDE_CHA).text)[0])
    stats["LEFT"]["HP"] = int(re.findall(r"\d+", browser.find_element("xpath", LEFTSIDE_HP).text)[0])
    stats["LEFT"]["AC"] = int(re.findall(r"\d+", browser.find_element("xpath", LEFTSIDE_AC).text)[0])
    stats["LEFT"]["SPEED"] = int(re.findall(r"\d+", browser.find_element("xpath", LEFTSIDE_SPEED).text)[0])


    left_plaintext = browser.find_element("xpath", LEFTSIDE_STATS).text.split("\n")[10:]

    stats["LEFT"]["WINS"] = []
    stats["LEFT"]["RESIST"] = []        
    stats["LEFT"]["VULNERABLE"] = []        
    stats["LEFT"]["IMMUNE"] = []
    stats["LEFT"]["ABSORB"] = []
    stats["LEFT"]["ACTIONS"] = []
    stats["LEFT"]["CONDITIONS"] = []
    stats["LEFT"]["MISC"] = []

    pointer = "MISC"

    for attribute in left_plaintext:
        if is_caps(attribute):
            pointer = attribute
        else:
            stats["LEFT"][pointer].append(attribute)
    
    # * Formatting

    try:
        stats["LEFT"]["WINS"] = stats["LEFT"]["WINS"][0].split(", ")
    except:
        pass
    try:
        stats["LEFT"]["RESIST"] = stats["LEFT"]["RESIST"][0].split(", ")
    except:
        pass
    try:
        stats["LEFT"]["VULNERABLE"] = stats["LEFT"]["VULNERABLE"][0].split(", ")
    except:
        pass
    try:
        stats["LEFT"]["IMMUNE"] = stats["LEFT"]["IMMUNE"][0].split(", ")
    except:
        pass
    try:
        stats["LEFT"]["ABSORB"] = stats["LEFT"]["ABSORB"][0].split(", ")
    except:
        pass

    stats = parse_attacks("LEFT", stats)

    

    #* _______RIGHTSIDE_________

    stats["RIGHT"]["STR"] = int(re.findall(r"\d+", browser.find_element("xpath", RIGHTSIDE_STR).text)[0])
    stats["RIGHT"]["DEX"] = int(re.findall(r"\d+", browser.find_element("xpath", RIGHTSIDE_DEX).text)[0])
    stats["RIGHT"]["CON"] = int(re.findall(r"\d+", browser.find_element("xpath", RIGHTSIDE_CON).text)[0])
    stats["RIGHT"]["INT"] = int(re.findall(r"\d+", browser.find_element("xpath", RIGHTSIDE_INT).text)[0])
    stats["RIGHT"]["WIS"] = int(re.findall(r"\d+", browser.find_element("xpath", RIGHTSIDE_WIS).text)[0])
    stats["RIGHT"]["CHA"] = int(re.findall(r"\d+", browser.find_element("xpath", RIGHTSIDE_CHA).text)[0])
    stats["RIGHT"]["HP"] = int(re.findall(r"\d+", browser.find_element("xpath", RIGHTSIDE_HP).text)[0])
    stats["RIGHT"]["AC"] = int(re.findall(r"\d+", browser.find_element("xpath", RIGHTSIDE_AC).text)[0])
    stats["RIGHT"]["SPEED"] = int(re.findall(r"\d+", browser.find_element("xpath", RIGHTSIDE_SPEED).text)[0])


    right_plaintext = browser.find_element("xpath", RIGHTSIDE_STATS).text.split("\n")[10:]

    stats["RIGHT"]["WINS"] = []
    stats["RIGHT"]["RESIST"] = []        
    stats["RIGHT"]["VULNERABLE"] = []        
    stats["RIGHT"]["IMMUNE"] = []
    stats["RIGHT"]["ABSORB"] = []
    stats["RIGHT"]["ACTIONS"] = []
    stats["RIGHT"]["CONDITIONS"] = []
    stats["RIGHT"]["MISC"] = []

    pointer = "MISC"

    for attribute in right_plaintext:
        if is_caps(attribute):
            pointer = attribute
        else:
            stats["RIGHT"][pointer].append(attribute)
    
    # * Formatting

    try:
        stats["RIGHT"]["WINS"] = stats["RIGHT"]["WINS"][0].split(", ")
    except:
        pass
    try:
        stats["RIGHT"]["RESIST"] = stats["RIGHT"]["RESIST"][0].split(", ")
    except:
        pass
    try:
        stats["RIGHT"]["VULNERABLE"] = stats["RIGHT"]["VULNERABLE"][0].split(", ")
    except:
        pass
    try:
        stats["RIGHT"]["IMMUNE"] = stats["RIGHT"]["IMMUNE"][0].split(", ")
    except:
        pass
    try:
        stats["RIGHT"]["ABSORB"] = stats["RIGHT"]["ABSORB"][0].split(", ")
    except:
        pass

    stats = parse_attacks("RIGHT", stats)
    
    # * CALCULATING AVERAGE DAMAGES

    
    stats = determine_dpr("LEFT", stats)
        
    stats = determine_dpr("RIGHT", stats)

    for stat in stats["LEFT"]:
        print(f"{stat}: {stats['LEFT'][stat]}")  
    print("") 

    for stat in stats["RIGHT"]:
        print(f"{stat}: {stats['RIGHT'][stat]}")  
    print("") 

    return stats

def apply_ac_conditions(side: str, stats: dict, ac: int) -> int:
    if side == "LEFT":
        other = "RIGHT"
    else:
        other = "LEFT"

    # Own side conditions that lower/increase AC
    if "Mage Armor" in stats[side]["ACTIONS_PARSED"]:
        ac = max(ac, 13 + (stats[side]["DEX"] - 10)//2)
    if "Blessed" in stats[side]["CONDITIONS"]:
        ac += 2
    if "Blessed By God" in stats[side]["CONDITIONS"]:
        ac += 2
    if "Shield" in stats[side]["ACTIONS_PARSED"]:
        ac += 3 # ! NOT 5 because it can't use it more than once. I can't implement that feature directly so I'm  estimating it to be a +3 increase in AC
    if "Parry" in stats[side]["ACTIONS_PARSED"]:
        ac += 2
    if "Greater Invisibile" in stats[side]["CONDITIONS"] and "True Sight" not in stats[other]["CONDITIONS"]:
        ac += 3

    # Other side conditions that lower/increase effective AC
    if "Frenzied" in stats[other]["CONDITIONS"]:
        ac -= 3
    if "Power Attacker" in stats[other]["CONDITIONS"]:
        ac += 4
    if "Greater Invisibile" in stats[other]["CONDITIONS"] and "True Sight" not in stats[side]["CONDITIONS"]:
        ac -= 3
    
    return ac

def apply_health_conditions(side: str, stats: dict, hp: int) -> int:
    if "Regeneration" in stats[side]["CONDITIONS"]:
        hp += 8
    if "5 Heads" in stats[side]["CONDITIONS"]:
        hp += 20
    return hp

def calc_tougher(right_name:str, left_name:str) -> float:

    stats = get_stats(right_name, left_name)

    if check_PC(stats):
        print("One of the combatants is a PC. Skipping bet.")
        return 1.0
    
    # TODO: estimating to-hit is based off of stats instead of attacks for some reason. This doesn't take into account Power Hitter or Advantage. Implement those
    left_ac = int(re.findall(
        r"\d+", browser.find_element("xpath", LEFTSIDE_AC).text)[0])
    left_estimated_to_hit = max(int(
        (int(re.findall(r"\d+", browser.find_element("xpath", LEFTSIDE_STR).text)[0]) - 6)/2), int(
        (int(re.findall(r"\d+", browser.find_element("xpath", LEFTSIDE_DEX).text)[0]) - 6)/2))

    right_ac = int(re.findall(
        r"\d+", browser.find_element("xpath", RIGHTSIDE_AC).text)[0])
    right_estimated_to_hit = max(int(
        (int(re.findall(r"\d+", browser.find_element("xpath", RIGHTSIDE_STR).text)[0]) - 6)/2), int(
        (int(re.findall(r"\d+", browser.find_element("xpath", RIGHTSIDE_DEX).text)[0]) - 6)/2))

    left_effective_ac = left_ac - right_estimated_to_hit
    right_effective_ac = right_ac - left_estimated_to_hit

    left_effective_ac = apply_ac_conditions("LEFT", stats, left_effective_ac)    
    right_effective_ac = apply_ac_conditions("RIGHT", stats, right_effective_ac)    

    print(f"Left AC:{left_effective_ac}; Right AC: {right_effective_ac}")

    left_hp = int(re.findall(r"\d+", browser.find_element("xpath", LEFTSIDE_HP).text)[0])
    right_hp = int(re.findall(r"\d+", browser.find_element("xpath", RIGHTSIDE_HP).text)[0])

    left_hp = apply_health_conditions("LEFT", stats, left_hp)
    right_hp = apply_health_conditions("RIGHT", stats, right_hp)
    
    left_toughness = max(1/20, min(1, 20/(20-left_effective_ac))) * left_hp

    left_toughness /= stats["RIGHT"]["DPR"]

    right_toughness = max(1/20, min(1, 20/(20-right_effective_ac))) * right_hp

    right_toughness /= stats["LEFT"]["DPR"]
    
    print(
        f"Left expected number of rounds survived:{left_toughness}; Right expected number of rounds survived: {right_toughness}")

    ratio = left_toughness / right_toughness

    if ratio > 1/0.9:
        ratio_unlucky = left_toughness / (right_toughness + 0.5)
        if ratio_unlucky < 1:
            print("Bot: Left side should win, but a single bad round could change that.")
            ratio = 1.0
    elif ratio < 0.9:
        ratio_unlucky = (left_toughness + 0.5) / right_toughness
        if ratio_unlucky > 1:
            print("Bot: Right side should win, but a single bad round could change that.")
            ratio = 1.0

    return ratio

def plot_scores(score):
    score_history.append(int(score))
    plt.plot(score_history, marker='o')
    plt.title('Score History')
    plt.xlabel('Bets')
    plt.ylabel('Score (GP)')
    plt.grid()
    plt.pause(0.1)  # Pause to allow the plot to update
    plt.show()

def run():
    if betting():
        print("\n\n---------------BETTING---------------")

        browser.refresh()

        wait_for_bets_score_not_zero(browser)

        score = browser.find_element("class name", "BetsScore").text

        print(f"Score: {score}GP")

        try:
            right_name = browser.find_element("xpath", RIGHTSIDENAME).text
        except:
            try:
                right_name = browser.find_element("xpath", RIGHTSIDENAMETWO).text
            except:
                right_name = "RIGHT"

        try:
            left_name = browser.find_element("xpath", LEFTSIDENAME).text
        except:
            try:
                left_name = browser.find_element("xpath", LEFTSIDENAMETWO).text
            except:
                left_name = "LEFT"

        print(f"Matchup:\n{left_name}  vs.  {right_name}")

        ratio = calc_tougher(right_name, left_name)

        if ratio < 1:

            confidence = 1-ratio

            print(f"Confidence: {confidence}")

            bet = int(int(score) * confidence) // 2

            if int(score) - bet <= 50:
                bet = int(score)
            

            if confidence < 0.1:
                print("Not confident enough to bet.")
                # chat("Not confident enough to bet.")
            else:
                plot_scores(score)
                try:

                    browser.find_element("xpath", RIGHTSIDEBET).clear()
                    browser.find_element("xpath", RIGHTSIDEBET).send_keys(str(bet))
                    browser.find_element("xpath", RIGHTSIDECOMMIT).click()
                    print(f"Bot: betting {bet/int(score) * 100}% ({bet} GP) on '{right_name}'")
                    # chat(f"Bot: betting {bet/int(score) * 100:.2f}% ({bet} GP) on '{right_name}'")

                    for browsertwo, i in zip(counterbetters, range(counterbettercount)):
                        browsertwo.find_element("xpath", LEFTSIDEBET).clear()
                        browsertwo.find_element("xpath", LEFTSIDEBET).send_keys("1")
                        browsertwo.find_element("xpath", LEFTSIDECOMMIT).click()
                        print(f"Bot {2+i} counterbet 1 GP")
                except:
                    print("Ran out of time before betting.")

            sleep(30)
        else:

            confidence = 1-1/ratio

            print(f"Confidence: {confidence}")

            bet = int(int(score) * confidence) // 2

            if int(score) - bet <= 50:
                bet = int(score)
            
            if confidence < 0.1:
                print("Not confident enough to bet.")
                # chat("Not confident enough to bet.")
            else:
                plot_scores(score)
                try:

                    browser.find_element("xpath", LEFTSIDEBET).clear()
                    browser.find_element("xpath", LEFTSIDEBET).send_keys(str(bet))
                    browser.find_element("xpath", LEFTSIDECOMMIT).click()
                    print(f"Bot: betting {bet/int(score) * 100}% ({bet} GP) on '{left_name}'")
                    # chat(f"Bot: betting {bet/int(score) * 100:.2f}% ({bet} GP) on '{left_name}'")

                    for browsertwo, i in zip(counterbetters, range(counterbettercount)):
                        browsertwo.find_element("xpath", RIGHTSIDEBET).clear()
                        browsertwo.find_element("xpath", RIGHTSIDEBET).send_keys("1")
                        browsertwo.find_element("xpath", RIGHTSIDECOMMIT).click()
                        print(f"Bot {2+i} counterbet 1 GP")
                except:
                    print("Ran out of time before betting.")
            sleep(30)
    # else:
    #     print("\n")


if __name__ == '__main__':
    opts = Options()
    optstwo = Options()
    optstwo.add_argument('--headless=new')
    browser = Firefox(options=opts)

    counterbettercount = 0
    counterbetters = [Firefox(options=optstwo) for _ in range(counterbettercount)]

    score_history = []

    plt.figure(figsize=(10, 6))
    plt.ion()  # Turn on interactive mode for live updates
    plt.yscale('log')

    login()
    login_two()
    while True:
        try:
            run()
        except Exception:
            traceback_output = traceback.format_exc()
            print(traceback_output)
        sleep(10)
    browser.quit()
    browsertwo.quit()
