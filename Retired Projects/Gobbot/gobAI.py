from GobDat.consts import *
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from math import sqrt, log, floor, log2
import numpy as np
import traceback
from matplotlib import pyplot as plt
from collections import Counter

import random as rd
import re

import json
import os
import time

from time import sleep

LOG_PATH = "training_log.jsonl"

# Set up Elo+Empirical model
from model_feats import MatchupModel, train_from_log
from model import MatchupModel as FeatlessModel
from model import train_from_log as featless_train
from monsters import MONSTER_ENUM, MONSTER_CR, CONDITION_ENUM

model = MatchupModel()
featlessmodel = FeatlessModel()
train_from_log(model)
featless_train(featlessmodel)

debug = True

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
    ax[0].plot(score_history, marker='o')
    ax[0].set_title('Score History')
    ax[0].set_xlabel('Bets')
    ax[0].set_ylabel('Score (GP)')
    ax[0].grid()
    plt.pause(0.1)  # Pause to allow the plot to update
    plt.show()

def plot_max_scores():
    log_bins = [floor(log2(v)) for v in max_history if v > 0]

    # Define integer-aligned bin edges
    bin_edges = [b - 0.5 for b in range(min(log_bins), max(log_bins) + 2)]

    ax[1].hist(log_bins, bins=bin_edges)
    ax[1].set_title('Maxima History')
    ax[1].set_xlabel("Score power of 2")
    ax[1].set_ylabel('Count')
    ax[1].set_xticks(range(min(log_bins), max(log_bins) + 1))

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
    global last_gp, max_gp,  pending_match, last_bet_on, wincount, last_confidence, matchcount, model, featlessmodel

    if betting():
        print("\n\n---------------BETTING---------------")

        browser.refresh()

        wait_for_bets_score_not_zero(browser)

        current_gp = get_current_gp()

        plot_scores(current_gp)
        if max_history:
            plot_max_scores()

        leftside_info, rightside_info = get_info()
        # Resolve previous match
        if pending_match is not None and last_gp is not None and last_bet_on is not None:
            if current_gp > last_gp:
                winner = last_bet_on
                max_gp = max(current_gp, max_gp)
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
                max_history.append(max_gp)
                score_history.clear()
                pending_match = None
                last_gp = None
                last_bet_on = None
                max_gp = 0
            else:
                log_entry = pending_match.copy()
                log_entry["winner"] = winner
                append_log(log_entry)

                if (last_confidence is not None):
                    # Update win and match counts
                    # new version: changed to split matchcount, wincount into arrays of 5 ints, incrementing for confidence brackets:
                    # 0 -> 50%-60%
                    # 1 -> 60%-70%
                    # 2 -> 70%-80%
                    # 3 -> 80%-90%
                    # 4 -> 90%-100%
                    last_confidence = min(max(last_confidence, 0.5), 0.99)
                    current_confidence_bracket = floor((last_confidence - 0.5) * 10)
                    matchcount[current_confidence_bracket] += 1
                    if winner == last_bet_on:
                        wincount[current_confidence_bracket] += 1
                
                model = MatchupModel()
                train_from_log(model)
                featlessmodel = FeatlessModel()
                featless_train(featlessmodel)
                # print("Retrained model from log.")
                
                pending_match = None
                last_gp = None
                last_bet_on = None
                last_confidence = None
        last_gp = current_gp

        print(f"Win Rate for confidence 50%-60% : {wincount[0]}/{matchcount[0]} ({(wincount[0]/matchcount[0]*100) if matchcount[0] > 0 else 0:.2f}%)")
        print(f"Win Rate for confidence 60%-70% : {wincount[1]}/{matchcount[1]} ({(wincount[1]/matchcount[1]*100) if matchcount[1] > 0 else 0:.2f}%)")
        print(f"Win Rate for confidence 70%-80% : {wincount[2]}/{matchcount[2]} ({(wincount[2]/matchcount[2]*100) if matchcount[2] > 0 else 0:.2f}%)")
        print(f"Win Rate for confidence 80%-90% : {wincount[3]}/{matchcount[3]} ({(wincount[3]/matchcount[3]*100) if matchcount[3] > 0 else 0:.2f}%)")
        print(f"Win Rate for confidence 90%-100%: {wincount[4]}/{matchcount[4]} ({(wincount[4]/matchcount[4]*100) if matchcount[4] > 0 else 0:.2f}%)")
        print(f"Total Win Rate: {sum(wincount)}/{sum(matchcount)} ({sum(wincount)/sum(matchcount) if sum(matchcount) > 0 else 0:.2f}%)")

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

        left = (MONSTER_ENUM[leftside_info[0]], CONDITION_ENUM[leftside_info[1]])
        right = (MONSTER_ENUM[rightside_info[0]], CONDITION_ENUM[rightside_info[1]])

        p_left_wins = model.predict(left, right, debug=debug)
        p_left_wins_featless = featlessmodel.predict(left, right, debug=debug)
        difference = p_left_wins - p_left_wins_featless
        if debug:
            print(f"After running both models, their prediction difference is {difference*100:.2f}.")

        if p_left_wins > 0.5:
            prediction = "LEFT"
            confidence = p_left_wins
        else:
            prediction = "RIGHT"
            confidence = 1-p_left_wins
        
        last_confidence = confidence

        # Temporary measure to not ruin the fun for others and intentionally lose tournaments
        current_left_cr = MONSTER_CR[leftside_info[0]]
        current_right_cr = MONSTER_CR[rightside_info[0]]

        # Calculate bet amount based on confidence and Kelly criterion
        if sum(matchcount) < 1000:
            # use pre-fit quadratic to adjust confidence early on when data is sparse, to avoid overbetting on high confidence predictions that aren't well-calibrated yet. After 1000 matches, the confidence should be more reliable so we can use it directly.
            confidence = -0.928571 * (confidence ** 2) + 2.19886 * confidence - 0.38265 # Readjusting confidence based on tests and best fit quadratic. TEMPORARY
        else:
            # fit a quadratic to the actual win rates in each confidence bracket, and use that to adjust confidence to be more accurate. This is because the raw model confidence isn't perfectly calibrated, especially in the early stages when data is sparse, and this adjustment helps improve betting decisions.
            fiftyfivepcwinrate = (wincount[0]/matchcount[0])
            sixtyfivepcwinrate = (wincount[1]/matchcount[1])
            seventyfivepcwinrate = (wincount[2]/matchcount[2])
            eightyfivepcwinrate = (wincount[3]/matchcount[3])
            ninetyfivepcwinrate = (wincount[4]/matchcount[4])
            # Fit a quadratic to these 5 points: (0.55, fiftyfivepcwinrate), (0.65, sixtyfivepcwinrate), (0.75, seventyfivepcwinrate), (0.85, eightyfivepcwinrate), (0.95, ninetyfivepcwinrate)
            x = [0.55, 0.65, 0.75, 0.85, 0.95]
            y = [fiftyfivepcwinrate, sixtyfivepcwinrate, seventyfivepcwinrate, eightyfivepcwinrate, ninetyfivepcwinrate]
            coeffs = np.polyfit(x, y, 2)
            a, b, c = coeffs
            confidence = a * (confidence ** 2) + b * confidence + c

        p = confidence
        q = 1 - p
        b = 0.5 + 0.5 * counterbettercount  # Adjusted odds based on number of counterbetters
        kelly_fraction = p - (q / b)
        kelly_fraction = max(0, min(kelly_fraction, 1))  # Clamp between 0 and 1

        if current_left_cr == 17 or current_right_cr == 17:
            if prediction == "LEFT":
                prediction = "RIGHT"
            else:
                prediction = "LEFT"
            bet = current_gp  # All-in to lose quickly
            last_confidence = None # don't log in winrate.
            print("Intentionally losing against CR 17 monster.")
        else:
            
            bet = int(current_gp * kelly_fraction)

            if bet < 1:
                bet = 1

            if current_gp - bet <= 50:
                bet = current_gp

            # if prediction == "LEFT" and rightside_info[1] == "Starts Invisible":
            #     bet = 1
            # elif prediction == "RIGHT" and leftside_info[1] == "Starts Invisible":
            #     bet = 1

        last_bet_on = prediction

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

    counterbettercount = 1
    counterbetters = [Firefox(options=optstwo) for _ in range(counterbettercount)]

    score_history = []
    max_history = []
    last_gp = None
    max_gp = 0
    pending_match = None
    wincount = [0, 0, 0, 0, 0]
    matchcount = [0, 0, 0, 0, 0]
    last_confidence = None

    fig, ax = plt.subplots(2, 1)
    plt.ion()  # Turn on interactive mode for live updates
    fig.set_figheight(10)
    fig.set_figwidth(15)

    
    ax[0].set_yscale('log', base=2)
    # ax[1].set_yscale('log', base=2)

    login()
    login_two()
    while True:
        try:
            run()
        except Exception:
            traceback_output = traceback.format_exc()
            print(traceback_output)
        sleep(10)
