from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from base64 import b64decode, b32decode
import re
from datetime import datetime
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.alert import Alert
# from selenium.common.exceptions import NoAlertPresentException

import random

from cypherKotH.consts import *

import time

opts = Options()
opts.headless = False
browser = Firefox(options=opts)

def run():
    global totalflags
    browser.get(HILLURL)

    try:
        king = browser.find_element_by_id("king").text.split(' ')[-1]
    except:
        try:
            if browser.find_element_by_xpath(F01LOCATION).text != "Not Authorized":
                king = "peasants"
            else:
                login()
                browser.get(HILLURL)
                return
        except:
            login()
            browser.get(HILLURL)
            return

    if king != 'Bravo':
        print(f"Dethroning {king}")
        thetext = browser.find_element_by_id("ciphertext").text

        cyphertype = identify_cypher(thetext)

        flag = decode(thetext, cyphertype)
        print(f"The flag was {flag}")

        browser.find_element_by_xpath(FLAGINPUTLOCATION).send_keys(flag)
        browser.find_element_by_xpath(FLAGBUTTON).click()
        totalflags += 1
    else:
        print(f"We are King! Total captures: {totalflags}")
    print(datetime.now().strftime("%H:%M:%S"))


def login() -> None:
    browser.get(LOGINURL)

    browser.implicitly_wait(20)

    browser.find_element_by_xpath(USERNAMEBUTTON).send_keys(USERNAME)
    browser.find_element_by_xpath(PASSWORDBUTTON).send_keys(PASS)
    browser.find_element_by_xpath(REMEMBERBUTTON).click()
    browser.find_element_by_xpath(LOGINBUTTON).click()

    browser.implicitly_wait(20)


def identify_cypher(cypherstring) -> str:
    if vign(cypherstring[-14:], 'N')[:6] == "icrCTF":
        return "rot13"
    elif ' ' not in cypherstring and 'a' in cypherstring:
        return "base64"
    elif ' ' not in cypherstring and 'a' not in cypherstring:
        return "base32"
    elif 'C' not in cypherstring and "{" in cypherstring:
        return "morse"
    else:
        return "Vigenere"


def vign(text: str, key: str) -> str:
    text = text[-14:]
    text = text.replace('{', '')
    text = text.replace('}', '')
    orig_text = []
    for i in range(len(text)):
        if ord(text[i]) > 96:
            x = (ord(text[i]) - ord(key.lower()[i % len(key)]) + 26) % 26
            x += ord('a')
        else:
            x = (ord(text[i]) - ord(key[i % len(key)]) + 26) % 26
            x += ord('A')
        orig_text.append(chr(x))
    res = "" . join(orig_text)
    return res[:6] + "{" + res[-6:] + "}"


def morse(morseletters) -> str:

    flagletters = ''
    for letter in morseletters:
        flagletters += MORSELETTERS[letter]
    return "icrCTF{" + flagletters + "}"


def bacon(baconletters) -> str:
    flagletters = ''
    for letter in baconletters:
        flagletters += BACONLETTERS[letter]
    return "icrCTF{" + flagletters + "}"


def get_vign_key(flag) -> str:
    key = ""
    sol = "icrCTF"

    for i in range(4):
        diff = ord(flag[i])-ord(sol[i])
        if diff < 0:
            diff += 26
        elif diff > 26:
            diff -= 26
        key += chr(diff + ord('A'))

    return key


def decode(cypherstring, cyphertype) -> str:

    try:
        if cyphertype == "rot13":
            print("rot13")
            return vign(cypherstring, "N")
        elif cyphertype == "Vigenere":
            print("It was vigenere.")

            key = get_vign_key(cypherstring[-14:])

            print(f"The key was {key}")

            flag = vign(cypherstring, key)

            return flag
        elif cyphertype == 'base64':
            
            print("64'ing it up here!")
            decoded = str(b64decode(cypherstring))

            flag = re.findall(CYPHERFORMAT, decoded)

            return flag[0]
        elif cyphertype == 'base32':
            print("32'ing it up here!")
            decoded = str(b32decode(cypherstring))

            flag = re.findall(CYPHERFORMAT, decoded)
            return flag[0]
        elif cyphertype == 'morse':
            try:
                flag = morse(re.findall(MORSECYPHERFORMAT, cypherstring)[0])
                print("beep beep beep boop boop boop beep beep beep")
            except:
                print("Haram Cypher oh no")
                flag = bacon(re.findall(BACONCYPHERFORMAT, cypherstring)[0])
            return flag
        # print(cypherstring)
        return "ERROR"
    except Exception as e:
        print(e + "\n")
        # print(cypherstring)
        return "ERROR"


if __name__ == '__main__':
    login()
    totalflags = 0
    while True:
        run()
        time.sleep(10800)
