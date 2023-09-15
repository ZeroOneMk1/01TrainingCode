from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

opts = Options()
# opts.add_argument('-headless')
browser = Firefox(options=opts)

browser.get("https://www.lyrical-nonsense.com/lyrics/hachi-vsinger/honey-bees/")

lyrics_o = browser.find_element(By.CLASS_NAME, "olyrictext").text

print("a")

# print(lyrics_o.decode("utf-8"))