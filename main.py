import nltk
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize

import pronouncing
import lyricsgenius
import random
import string
import json
import os
import re

TDATA_FN = "training_data\inputs"

def get_random_rhyme(word):
    rhymes = pronouncing.rhymes(word)
    return random.choice(rhymes)


def extract_rhymes(data):
    """
    Given a string of lyrics, tokenize them and return the last word of each line.
    NOTE: for now we are naively assuming that only the last line contains a rhyme.
    """
    cleaned_data = data.translate(str.maketrans('', '', string.punctuation)).split('\n')
    tokens = [wordpunct_tokenize(word) for word in cleaned_data]
    last = [ sentence[len(sentence) - 1] for sentence in tokens]

    return last

def get_credentials():
    with open("credentials.json", "r") as read_data:
        creds = json.load(read_data)
    return creds

def artist_in_training_data():
    return False

def create_lyrics_data(song):
    song_title = re.sub("\s", "_", song.title)
    artist_name = re.sub("\s", "_", song.artist)
    output_filepath = TDATA_FN + "\\" + artist_name + "\\" + song_title + ".txt"
    lyrics = re.sub("-", " ", song.lyrics)
    lyrics = re.sub("([\(\[]).*?([\)\]])", "", lyrics)

    if not os.path.exists(TDATA_FN + "\\" + artist_name):
        os.makedirs(TDATA_FN + "\\" + artist_name)

    
    output_fd = open(output_filepath, "w")
    output_fd.write(lyrics)
    output_fd.close()

def main():
    creds = get_credentials()
    artist_name = 'Kanye West'

    

    if (not artist_in_training_data()):
        session = lyricsgenius.Genius(creds['access_token'])
        artist = session.search_artist(artist_name, max_songs=3, sort='popularity')
        for song in artist.songs:
            create_lyrics_data(song)

        #fetch artist lyrics data


if __name__ == "__main__":
    main()
