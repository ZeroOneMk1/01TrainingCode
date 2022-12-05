from GobDat.consts import *
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from math import sqrt
import traceback

import random as rd
import re

from time import sleep

opts = Options()
optstwo = Options()
opts.headless = False
optstwo.headless = True
browser = Firefox(options=opts)
browsertwo = Firefox(options=optstwo)


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
        name = re.findall(r"([\w\ ]+):", action)[0]
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

                if stats[side]["ACTIONS_PARSED"][action]["TYPE"][i] in stats[other]["VULNERABLE"]:
                    dmg *= 2
                elif stats[side]["ACTIONS_PARSED"][action]["TYPE"][i] in stats[other]["RESIST"]:
                    dmg /= 2
                elif stats[side]["ACTIONS_PARSED"][action]["TYPE"][i] in stats[other]["IMMUNE"] or stats[side]["ACTIONS_PARSED"][action]["TYPE"][i] in stats[other]["ABSORB"]:
                    dmg = 0
                
                stats[side]["ACTIONS_PARSED"][action]["DAMAGE"] += dmg
    
    for action in stats[side]["ACTIONS_PARSED"]:
        if "Multi" in action:
            dmg = 0
            for attack in stats[side]["ACTIONS_PARSED"][action]["ACTIONS"]:
                try:
                    multiplier = int(attack[0])
                    dmg += multiplier * stats[side]["ACTIONS_PARSED"][attack[2:]]["DAMAGE"]
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

def login() -> None:

    browser.get(LOGINURL)

    sleep(4)

    browser.find_element("xpath", LOGINLOCATION).click()

    browser.find_element("xpath", USERNAMEBUTTON).send_keys(EMAIL)
    browser.find_element("xpath", PASSWORDBUTTON).send_keys(PASS)

    browser.find_element("xpath", LOGINBUTTON).click()

    sleep(4)

    browser.find_element("xpath", CONTINUEBUTTON).click()

def login_two() -> None:

    browsertwo.get(LOGINURL)

    sleep(4)

    browsertwo.find_element("xpath", LOGINLOCATION).click()

    browsertwo.find_element("xpath", USERNAMEBUTTON).send_keys(EMAILTWO)
    browsertwo.find_element("xpath", PASSWORDBUTTON).send_keys(PASSTWO)

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
    if "Blessed" in stats[side]["CONDITIONS"]:
        ac += 2
    if "Shield" in stats[side]["ACTIONS_PARSED"]:
        ac += 3 # ! NOT 5 because it can't use it more than once. I can't implement that feature directly so I'm  estimating it to be a +3 increase in AC
    if "Parry" in stats[side]["ACTIONS_PARSED"]:
        ac += 2
    if "Frenzied" in stats[other]["CONDITIONS"]:
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

    return ratio


def run():
    if betting():
        print("\n\n---------------BETTING---------------")

        browser.refresh()

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

            bet = int(int(score) * confidence)

            if int(score) - bet <= 50:
                bet = int(score)
            

            if confidence < 0.1:
                print("Not confident enough to bet.")
            else:
                try:

                    browser.find_element("xpath", RIGHTSIDEBET).clear()
                    browser.find_element("xpath", RIGHTSIDEBET).send_keys(str(bet))
                    browser.find_element("xpath", RIGHTSIDECOMMIT).click()
                    print(f"Bot: betting {bet/int(score) * 100}% ({bet} GP) on '{right_name}'")

                    browsertwo.find_element("xpath", RIGHTSIDEBET).clear()
                    browsertwo.find_element("xpath", RIGHTSIDEBET).send_keys("1")
                    browsertwo.find_element("xpath", RIGHTSIDECOMMIT).click()
                    print("Bot 2 counterbet 1 GP")
                except:
                    print("Ran out of time before betting.")

            sleep(30)
        else:

            confidence = 1-1/ratio

            print(f"Confidence: {confidence}")

            bet = int(int(score) * confidence)

            if int(score) - bet <= 50:
                bet = int(score)
            
            if confidence < 0.1:
                print("Not confident enough to bet.")
            else:
                try:

                    browser.find_element("xpath", LEFTSIDEBET).clear()
                    browser.find_element("xpath", LEFTSIDEBET).send_keys(str(bet))
                    browser.find_element("xpath", LEFTSIDECOMMIT).click()
                    print(f"Bot: betting {bet/int(score) * 100}% ({bet} GP) on '{left_name}'")

                    browsertwo.find_element("xpath", RIGHTSIDEBET).clear()
                    browsertwo.find_element("xpath", RIGHTSIDEBET).send_keys("1")
                    browsertwo.find_element("xpath", RIGHTSIDECOMMIT).click()
                    print("Bot 2 counterbet 1 GP")
                except:
                    print("Ran out of time before betting.")

            sleep(30)
    # else:
    #     print("\n")


if __name__ == '__main__':
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
