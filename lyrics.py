from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
import os
import shutil
import json


output_dir = 'Lyrics'

BASE_URL = 'https://api.musixmatch.com/ws/1.1'
API_KEY = '29857e86424cd1ed4941b631e2fa8651'


def get_lyrics(song_name):
    req = requests.get(
        f'{BASE_URL}/track.search?q_lyrics={song_name}&apikey={API_KEY}')
    res = json.loads(req.content)
    track_list = res['message']['body']['track_list']

    if len(track_list) == 0:
        return None

    track_id = track_list[0]['track']['track_id']
    req = requests.get(
        f'{BASE_URL}/track.lyrics.get?track_id={track_id}&apikey={API_KEY}')
    res = json.loads(req.content)

    return res['message']['body']['lyrics']['lyrics_body']


def write_lyric_file(song_name, lyrics):
    with open(f'Lyrics/{song_name}.txt', "w", encoding="utf-8") as f:
        f.write(lyrics)
        f.close()


def main():
    os.mkdir(output_dir)
    songs = os.listdir('o')
    songs_lyrics = [
        {'name': song, 'lyrics': get_lyrics(song[0:-4])} for song in songs]

    for song in songs_lyrics:
        write_lyric_file(song['name'], str(song['lyrics']))


if __name__ == '__main__':
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    main()
