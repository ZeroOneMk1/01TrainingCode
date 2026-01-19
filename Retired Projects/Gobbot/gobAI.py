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

import json
import os
import time

from time import sleep

LOG_PATH = "training_log.jsonl"

# Set up Elo+Empirical model
from model import MatchupModel, train_from_log
from monsters import MONSTER_ENUM, MONSTER_CR

model = MatchupModel()
train_from_log(model)

## Helpers ##
def append_log(entry: dict):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
        f.flush()
        os.fsync(f.fileno())


def wait_for_bets_score_not_zero(driver, timeout=10):
    """Waits until an element with class 'BetsScore' has non-zero text."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda driver: driver.find_element(By.CLASS_NAME, "BetsScore").text != "0"
        )
        sleep(1)  # Small delay to ensure stability
        return True  # Element found and has non-zero text
    except TimeoutException:
        print("Timeout: BetsScore element did not become non-zero within the specified time.")
        return False # element was not found, or text was never non-zero

def is_caps(string: str) -> bool:
    for char in string:
        if ord(char) < ord('A') or ord(char) > ord('Z'):
            return False
    return True

def betting() -> bool:
    try:
        browser.find_element("class name", "WelcomeStart").click()
        sleep(1)
    except:
        pass
    return browser.find_element("xpath", BETTINGBANNER).text == "PLACE YOUR BET"

def get_current_gp() -> int:
    return int(browser.find_element("class name", "BetsScore").text)

def plot_scores(score):
    score_history.append(int(score))
    plt.plot(score_history, marker='o')
    plt.title('Score History')
    plt.xlabel('Bets')
    plt.ylabel('Score (GP)')
    plt.grid()
    plt.pause(0.1)  # Pause to allow the plot to update
    plt.show()

def login() -> None:

    browser.get(LOGINURL)

    sleep(4)

    browser.find_element("xpath", LOGINLOCATION).click()

    browser.find_element("xpath", USERNAMEBUTTON).send_keys(COUNTEREMAILS[0])
    browser.find_element("xpath", PASSWORDBUTTON).send_keys(COUNTERPASSES[0])

    browser.find_element("xpath", LOGINBUTTON).click()

    sleep(4)
    
    try:
        browser.find_element("xpath", CONTINUEBUTTON).click()
    except:
        print("EXCEPTED: No continue button found.")
        browser.find_element("xpath", CONTINUEBUTTON_ASCENT).click()

def login_two() -> None:

    for browsertwo, i in zip(counterbetters, range(counterbettercount)):
        browsertwo.get(LOGINURL)

        sleep(4)

        browsertwo.find_element("xpath", LOGINLOCATION).click()

        browsertwo.find_element("xpath", USERNAMEBUTTON).send_keys(COUNTEREMAILS[i+1])
        browsertwo.find_element("xpath", PASSWORDBUTTON).send_keys(COUNTERPASSES[i+1])

        browsertwo.find_element("xpath", LOGINBUTTON).click()

        sleep(4)

        browsertwo.find_element("xpath", CONTINUEBUTTON).click()

def get_info() -> tuple:
    try:
        if "ADOPTED" in browser.find_element("xpath", RIGHTSIDEISOWNED).text:
            right_name = browser.find_element("xpath", RIGHTSIDENAMEWHENOWNED).text
        else:
            right_name = browser.find_element("xpath", RIGHTSIDENAME).text
    except:
        try:
            right_name = browser.find_element("xpath", RIGHTSIDENAME).text
        except:
            try:
                right_name = browser.find_element("xpath", RIGHTSIDENAMETWO).text
            except:
                right_name = "RIGHT"

    try:
        if "ADOPTED" in browser.find_element("xpath", LEFTSIDEISOWNED).text:
            left_name = browser.find_element("xpath", LEFTSIDENAMEWHENOWNED).text
        else:
            left_name = browser.find_element("xpath", LEFTSIDENAME).text
    except:
        try:
            left_name = browser.find_element("xpath", LEFTSIDENAME).text
        except:
            try:
                left_name = browser.find_element("xpath", LEFTSIDENAMETWO).text
            except:
                left_name = "LEFT"
    
    stats = {"LEFT": {}, "RIGHT": {}}
    try:
        stats["RIGHT"]["WINS"] = []
        stats["RIGHT"]["RESIST"] = []        
        stats["RIGHT"]["VULNERABLE"] = []        
        stats["RIGHT"]["IMMUNE"] = []
        stats["RIGHT"]["ABSORB"] = []
        stats["RIGHT"]["ACTIONS"] = []
        stats["RIGHT"]["CONDITIONS"] = []
        stats["RIGHT"]["MISC"] = []

        pointer = "MISC"
        
        right_plaintext = browser.find_element("xpath", RIGHTSIDE_STATS).text.split("\n")[10:]
        
        for attribute in right_plaintext:
            if is_caps(attribute):
                pointer = attribute
            else:
                stats["RIGHT"][pointer].append(attribute)

        right_alt_condition = stats["RIGHT"]["CONDITIONS"][0] if len(stats["RIGHT"]["CONDITIONS"]) > 0 else ""
    except:
        print("Failed to parse RIGHT stats.")

    try:
        stats["LEFT"]["WINS"] = []
        stats["LEFT"]["RESIST"] = []        
        stats["LEFT"]["VULNERABLE"] = []        
        stats["LEFT"]["IMMUNE"] = []
        stats["LEFT"]["ABSORB"] = []
        stats["LEFT"]["ACTIONS"] = []
        stats["LEFT"]["CONDITIONS"] = []
        stats["LEFT"]["MISC"] = []

        pointer = "MISC"
        
        left_plaintext = browser.find_element("xpath", LEFTSIDE_STATS).text.split("\n")[10:]
        
        for attribute in left_plaintext:
            if is_caps(attribute):
                pointer = attribute
            else:
                stats["LEFT"][pointer].append(attribute)

        left_alt_condition = stats["LEFT"]["CONDITIONS"][0] if len(stats["LEFT"]["CONDITIONS"]) > 0 else ""
    except:
        print("Failed to parse LEFT stats.")

    leftside_info = (left_name, left_alt_condition)
    rightside_info = (right_name, right_alt_condition)

    return leftside_info, rightside_info

def run():
    global last_gp, pending_match, last_bet_on, wincount, matchcount, model

    if betting():
        print("\n\n---------------BETTING---------------")

        browser.refresh()

        wait_for_bets_score_not_zero(browser)

        current_gp = get_current_gp()

        plot_scores(current_gp)

        leftside_info, rightside_info = get_info()

        # Resolve previous match
        if pending_match is not None and last_gp is not None and last_bet_on is not None:
            if current_gp > last_gp:
                winner = last_bet_on
            else:
                winner = "RIGHT" if last_bet_on == "LEFT" else "LEFT"

            # Check for tournament reset: if current monsters are low CR (<=0) and previous were high CR (>=10)
            prev_left_cr = MONSTER_CR.get(pending_match["left_monster"], 0)
            prev_right_cr = MONSTER_CR.get(pending_match["right_monster"], 0)
            current_left_cr = MONSTER_CR.get(leftside_info[0], 0)
            current_right_cr = MONSTER_CR.get(rightside_info[0], 0)
            
            max_prev_cr = max(prev_left_cr, prev_right_cr)
            max_current_cr = max(current_left_cr, current_right_cr)
            
            if max_current_cr <= 0 and max_prev_cr >= 10:
                print("Detected tournament reset (CR drop from high to low), skipping log for previous match.")
                pending_match = None
            else:
                log_entry = pending_match.copy()
                log_entry["winner"] = winner
                append_log(log_entry)
                pending_match = None

                # Update win and match counts
                matchcount += 1
                if winner == last_bet_on:
                    wincount += 1
                
                if (matchcount > 0): # matchcount % 10 == 0 and 
                    model = MatchupModel()
                    train_from_log(model)
                    print("Retrained model from log.")

        last_gp = current_gp

        print(f"Win Rate: {wincount}/{matchcount} ({(wincount/matchcount*100) if matchcount > 0 else 0:.2f}%)")

        print(f"Score: {current_gp}GP")

        pending_match = {
            "timestamp": time.time(),
            "left_monster": leftside_info[0],
            "left_condition": leftside_info[1],
            "right_monster": rightside_info[0],
            "right_condition": rightside_info[1]
        }

        print(f"Matchup:\n{leftside_info[0]}  vs.  {rightside_info[0]}")
        print(f"Conditions:\n{leftside_info[1]}  vs.  {rightside_info[1]}")

        # prediction, ratio = ai_predict(leftside_info, rightside_info)

        # print(f"Prediction: {prediction} with confidence ratio {ratio}")

        # ! TURN OFF WHEN NOT TRAINING ANYMORE
        # prediction = "LEFT"
        a = MONSTER_ENUM[leftside_info[0]]
        b = MONSTER_ENUM[rightside_info[0]]

        p_left_wins = model.predict(a, b, debug=True)

        if p_left_wins > 0.5:
            prediction = "LEFT"
        else:
            prediction = "RIGHT"

        # Temporary measure to not ruin the fun for others and intentionally lose tournaments
        current_left_cr = MONSTER_CR.get(leftside_info[0], 0)
        current_right_cr = MONSTER_CR.get(rightside_info[0], 0)
        if current_left_cr == 17 or current_right_cr == 17:
            if prediction == "LEFT":
                prediction = "RIGHT"
            else:
                prediction = "LEFT"
            bet = current_gp  # All-in to lose quickly
            print("Intentionally losing against CR 17 monster.")
        else:

            last_bet_on = prediction

            # Calculate bet amount based on confidence and Kelly criterion
            p = p_left_wins if prediction == "LEFT" else (1 - p_left_wins)
            q = 1 - p
            b = 0.5 + 0.5 * counterbettercount  # Adjusted odds based on number of counterbetters
            kelly_fraction = p - (q / b)
            kelly_fraction = max(0, min(kelly_fraction, 1))  # Clamp between 0 and 1
            bet = int(current_gp * kelly_fraction)

            if bet < 1:
                bet = 1

            if current_gp - bet <= 50:
                bet = current_gp

            if prediction == "LEFT" and rightside_info[1] == "Starts Invisible":
                bet = 1
            elif prediction == "RIGHT" and leftside_info[1] == "Starts Invisible":
                bet = 1

        if prediction == "RIGHT":
            try:
                browser.find_element("xpath", RIGHTSIDEBET).clear()
                browser.find_element("xpath", RIGHTSIDEBET).send_keys(str(bet))
                browser.find_element("xpath", RIGHTSIDECOMMIT).click()
                print(f"Bot: betting {bet/int(current_gp) * 100}% ({bet} GP) on '{rightside_info[0]}' (Kelly fraction: {kelly_fraction:.4f})")

                for browsertwo, i in zip(counterbetters, range(counterbettercount)):
                    browsertwo.find_element("xpath", LEFTSIDEBET).clear()
                    browsertwo.find_element("xpath", LEFTSIDEBET).send_keys("1")
                    browsertwo.find_element("xpath", LEFTSIDECOMMIT).click()
                    print(f"Bot {2+i} counterbet 1 GP")
            except Exception as e:
                print(f"Error during betting: {e}")
                pending_match = None
                # print("Ran out of time before betting.")
                sleep(30)
        else:
            try:
                browser.find_element("xpath", LEFTSIDEBET).clear()
                browser.find_element("xpath", LEFTSIDEBET).send_keys(str(bet))
                browser.find_element("xpath", LEFTSIDECOMMIT).click()
                print(f"Bot: betting {bet/int(current_gp) * 100}% ({bet} GP) on '{leftside_info[0]}' (Kelly fraction: {kelly_fraction:.4f})")

                for browsertwo, i in zip(counterbetters, range(counterbettercount)):
                    browsertwo.find_element("xpath", RIGHTSIDEBET).clear()
                    browsertwo.find_element("xpath", RIGHTSIDEBET).send_keys("1")
                    browsertwo.find_element("xpath", RIGHTSIDECOMMIT).click()
                    print(f"Bot {2+i} counterbet 1 GP")
            except Exception as e:
                print(f"Error during betting: {e}")
                # print("Ran out of time before betting.")
                sleep(30)


if __name__ == '__main__':
    opts = Options()
    optstwo = Options()
    optstwo.add_argument('--headless=new')
    browser = Firefox(options=opts)

    counterbettercount = 0
    counterbetters = [Firefox(options=optstwo) for _ in range(counterbettercount)]

    score_history = []
    last_gp = None
    pending_match = None
    wincount = 0
    matchcount = 0

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
