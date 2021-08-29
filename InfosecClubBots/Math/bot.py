from mathKotH.consts import *
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from base64 import b64decode, b32decode
from datetime import datetime

from time import sleep

opts = Options()
opts.headless = False
browser = Firefox(options=opts)

def parse(challengestring: str) -> float:
    parts = challengestring.split(" ")

    if parts[1] == '+':
        return float(parts[0]) + float(parts[2])
    elif parts[1] == '-':
        return float(parts[0]) - float(parts[2])
    elif parts[1] == '*':
        return float(parts[0]) * float(parts[2])
    elif parts[1] == '/':
        return float(parts[0]) / float(parts[2])
    elif parts[1] == '^':
        return float(parts[0]) ** float(parts[2])
    elif parts[1] == '%':
        return float(parts[0]) % float(parts[2])
    else:
        print(parts[1])
        raise ValueError

def login() -> None:
    browser.get(LOGINURL)

    browser.implicitly_wait(20)

    browser.find_element_by_xpath(USERNAMEBUTTON).send_keys(USERNAME)
    browser.find_element_by_xpath(PASSWORDBUTTON).send_keys(PASS)
    browser.find_element_by_xpath(REMEMBERBUTTON).click()
    browser.find_element_by_xpath(LOGINBUTTON).click()

    browser.implicitly_wait(20)

def run():
    global totalflags
    browser.get(HILLURL)
    try:
        king = browser.find_element_by_xpath(KINGLOCATION).text
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

    if TEAM not in king:
        challenge = browser.find_element_by_id("challenge").text
        challenge = challenge.split('=')[0]
        challenge = challenge.replace('Challenge: ', '')
        print(challenge)
        
        out = int(parse(challenge))

        print(out)

        browser.find_element_by_id("flag-in").send_keys("icrCTF{" + str(out) + "}")
        browser.find_element_by_xpath(FLAGBUTTON).click()
        totalflags += 1
    else:
        print(f"We are King! Total captures: {totalflags}")
    print(datetime.now().strftime("%H:%M:%S"))


if __name__ == '__main__':
    login()
    totalflags = 0
    while True:
        run()
        sleep(110)
    browser.quit()