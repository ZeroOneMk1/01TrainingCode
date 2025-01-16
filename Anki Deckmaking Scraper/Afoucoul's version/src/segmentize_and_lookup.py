#! /bin/env python3

import sys
import re
# import nagisa
import requests
import asyncio as aio
import json

# from os import listdir

API_URL = "https://jisho.org/api/v1/search/words?keyword={}"

# Define Unicode code point ranges for Hiragana, Katakana, and Han scripts
hiragana_range = r'\u3040-\u309F'
katakana_range = r'\u30A0-\u30FF'
han_range = r'\u4E00-\u9FFF'

PATH = '/Users/yusufsimsek/Desktop/Code/01TrainingCode/Anki Deckmaking Scraper/lyrics'

# Combine the ranges in the regex pattern
pattern = re.compile(f'[{hiragana_range}{katakana_range}{han_range}]+')
class ProgressBar:
    def __init__(self, high, size=50):
        self.high = high
        self.value = 0
        self.size = size

    def __str__(self):
        s = "|"
        s += ((20 * self.value) // self.high) * "█"
        s += ((20 * (self.high - self.value)) // self.high) * " "
        s += "|"
        s += " {}%".format(round(100 * self.value / self.high, 2))

        return s

    def increment(self):
        self.value += 1
        sys.stdout.write("\r{}".format(str(self)))
        sys.stdout.flush()
        

def validate_word(word):
    return (    
            not re.match(r'^\s*$', word)
            and not re.match(r'\W', word)
            and pattern.match(word)
            )


async def get_meaning(dictionary, word, progress_bar, origins):
    data = requests.get(API_URL.format(word)).json()['data'][0]

    reading = data['japanese'][0]['reading']
    meanings = [x['english_definitions'][0] for x in data['senses']]

    dictionary[word] = {'reading': reading, 'meanings': meanings} # , 'origin': origins[word]

    progress_bar.increment()


async def main(meanings):
    words = set()
    songlist = ['onomotopeia.txt']# listdir(PATH)
    words_origins = {}

    for song in songlist:

        with open(f'Anki Deckmaking Scraper/lyrics/{song}', 'r') as file:

            # songname = re.findall(r'([^.]+).[^.]+', song)[0]
            content = re.findall(pattern, file.read())
            for word in content:
                words.add(word)
            # for word in filter(
            #         validate_word,
            #         nagisa.wakati(content)):
            #     words.add(word)
                
                # try:
                #     if(songname not in words_origins[word]):
                #         words_origins[word].append(songname)
                # except:
                #     words_origins[word] = []
                #     words_origins[word].append(songname)
                
                # TODO find a way to remember which word came from which song
    
    with open("words.json", 'r') as f:
        try:
            existing_bank = json.load(f)
            for word in existing_bank:
                if word in words:
                    words.remove(word)
        except:
            pass


    print(f"Extracted {len(words)} new words\n\n")
    # print(words)

    progress_bar = ProgressBar(len(words))
    tasks = [aio.create_task(get_meaning(meanings, word, progress_bar, words_origins)) for word in words]
    await aio.wait(tasks)
    print("\nDone.")


if __name__ == '__main__':
    event_loop = aio.get_event_loop()
    try:
        meanings = {}

        with open("words.json", "r") as f:
            try:
                meanings = json.load(f)
            except:
                print("couldn't load meanings")

        event_loop.run_until_complete(main(meanings))

        # TODO store new words in extra bin

        with open("words.json", "w") as f:
            json.dump(meanings, f)

    finally:
        event_loop.close()
