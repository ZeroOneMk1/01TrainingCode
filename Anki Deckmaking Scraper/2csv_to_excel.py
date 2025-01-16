import json
import pandas as pd

# dict1 = {"number of storage arrays": 45, "number of ports":2390}

# 

# 

# 

# 

with open("words.json", "r") as f:
    words = json.load(f)

for word in words:
    words[word]['meanings'] = ', '.join(words[word]['meanings'])
    # words[word]['origin'] = ', '.join(words[word]['origin'])
df = pd.DataFrame(data=words)

df = (df.T)

print (df)

df.to_excel('Anki Deckmaking Scraper/dict1.xlsx')