from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import string
import re

from sudachipy import Dictionary, SplitMode

opts = Options()
# opts.add_argument('-headless')
browser = Firefox(options=opts)

# browser.get("https://www.lyrical-nonsense.com/lyrics/hachi-vsinger/honey-bees/")
browser.get(
    "https://www.lyrical-nonsense.com/lyrics/aiobahn-x-kotoko/internet-yamero/")

lyrics_o = browser.find_element(
    By.CLASS_NAME, "olyrictext").text.strip(string.punctuation)


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

browser.close()

tokenizer = Dictionary().create()

morphemes = tokenizer.tokenize(lyrics_o, SplitMode.A)
# print([m.surface() for m in morphemes])  # ['国会', '議事', '堂', '前', '駅']

with open("words.txt", 'w', encoding='utf-8') as f:
    f.write(str([m.surface() for m in morphemes]))