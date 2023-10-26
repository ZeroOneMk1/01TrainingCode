from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import string
import re



opts = Options()
# opts.add_argument('-headless')
# opts.add_argument("window-size=1920,1080")
opts.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
browser = Firefox(options=opts)

# browser.get("hachi-vsinger/honey-bees/""aiobahn-x-kotoko/internet-yamero/")

    
all_lyrics = ""
LINK_STEM = "https://www.lyrical-nonsense.com/lyrics/"
bands = ["kessoku-band", "hachi-vsinger", "hoshimachi-suisei", "yoasobi", "tokoyami-towa", "yorushika", "dustcell", "nanawo-akari", "ado", "zutto-mayonaka-de-ii-no-ni", "minami-373", "eve", "reol"]
songs = ["aiobahn-x-kotoko/internet-yamero", "aiobahn-x-kotoko/internet-overdose", "islet/hoshi-ni-naru-feat-isui", "yuika/juunanasai-no-uta", "the-binary/hana-ni-ame-wo-kimi-ni-uta-wo"]

for band in bands:
    try:
        browser.get(LINK_STEM+band+'/')

        curr_lyrics = [elem.get_attribute('innerHTML') for elem in browser.find_elements(By.CLASS_NAME,  "utdmobile")]
        curr_titles = [elem.get_attribute('innerHTML') for elem in browser.find_elements(By.CLASS_NAME,  "aptp_title")]
        curr_band = browser.find_elements(By.CLASS_NAME,  "titletext")[0].text

        for i in range(len(curr_titles)):
            song = curr_lyrics[i]
            song_name = curr_titles[i]
            with open(f"Anki Deckmaking Scraper/lyrics/{song_name} - {curr_band}.txt", 'w', encoding='utf-8') as f:
                f.write(song)


    except Exception as e:
        print(f"UNABLE TO STORE {band}\n\n{e}\n\n")

for song in songs:
    try:
        browser.get(LINK_STEM+song+'/')
        lyrics_o = browser.find_element(
            By.CLASS_NAME, "olyrictext").text
        song_name = browser.find_element(
            By.CLASS_NAME, "titletext").text
        
        curr_band = browser.find_element(
            By.CLASS_NAME, "titledet").text
        
        with open(f"Anki Deckmaking Scraper/lyrics/{song_name} - {curr_band}.txt", 'w', encoding='utf-8') as f:
                f.write(lyrics_o)
        # all_lyrics += f"{lyrics_o}\n\n"
    except:
        print(f"UNABLE TO STORE {song}")

# with open("lyrics_full.txt", 'w', encoding='utf-8') as f:
#     f.write(all_lyrics)

"""
lyrics_o = lyrics_o.strip(string.punctuation)

my_punct = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '.',
            '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_',
            '`', '{', '|', '}', '~', '»', '«', '“', '”', '…', '‥', '。', '「', '」', '【', '】', '、', '，', '゠', '＝', '『', '』', '〝', '〟', '⟨', '⟩', '〜', '：', '！', '？', '♪', '〽', 'ー', 'ﾟ',
            '０', '１', '２', '３', '４', '５', '６', '７', '８', '９',

            'Ａ', 'Ｂ', 'Ｃ', 'Ｄ', 'Ｅ', 'Ｆ', 'Ｇ', 'Ｈ', 'Ｉ', 'Ｊ', 'Ｋ', 'Ｌ', 'Ｍ', 'Ｎ', 'Ｏ', 'Ｐ', 'Ｑ', 'Ｒ', 'Ｓ', 'Ｔ', 'Ｕ', 'Ｖ', 'Ｗ', 'Ｘ', 'Ｙ', 'Ｚ',

            'ａ', 'ｂ', 'ｃ', 'ｄ', 'ｅ', 'ｆ', 'ｇ', 'ｈ', 'ｉ', 'ｊ', 'ｋ', 'ｌ', 'ｍ', 'ｎ', 'ｏ', 'ｐ', 'ｑ', 'ｒ', 'ｓ', 'ｔ', 'ｕ', 'ｖ', 'ｗ', 'ｘ', 'ｙ', 'ｚ',

            '，', '．', '：', '；', '！', '？', '＂', '＇', '｀', '＾', '～', '￣', '＿', '＆', '＠', '＃',

            '％', '＋', '－', '＊', '＝', '＜', '＞',

            '（', '）', '［', '］', '｛', '｝', '｟', '｠',

            '｜', '￤', '／', '＼', '￢',

            '＄', '￡', '￠', '￦', '￥']

punct_pattern = re.compile("[" + re.escape("".join(my_punct)) + "]")

lyrics_o = re.sub(r"[^\w]+", "", lyrics_o)

lyrics_o = re.sub(r"[a-zA-Z]+", "", lyrics_o)

lyrics_o = re.sub(punct_pattern, "", lyrics_o)

with open("lyrics_noeigo.txt", 'w', encoding='utf-8') as f:
    f.write(lyrics_o)
"""

browser.close()