import lyricsgenius
import json
import os
import re

TDATA_FN = "training_data\inputs"

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
    lyrics = re.sub("([\(\[]).*?([\)\]])", "", song.lyrics)

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
