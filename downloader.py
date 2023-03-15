from pytube import Playlist, YouTube
from termcolor import colored
from tqdm import tqdm
import moviepy.editor as mp
from concurrent.futures.process import ProcessPoolExecutor as Executor
import os
import shutil


# str(input('Playlist url: '))
playlist_url = 'https://www.youtube.com/playlist?list=PLV1qTAR8p8piVBzQncqjR7srgXuyUeQYU'
output_path = 'Trip'  # str(input('Output path: '))
playlist = Playlist(playlist_url)

print('Number of videos in playlist: %s' % len(playlist.video_urls))
print(colored('Downloading playlist: ', 'yellow') + playlist.title)


def download_song(video_url):
    video = YouTube(video_url)
    print(colored('Downloading ', 'green') + video.title)

    stream = video.streams.get_audio_only()

    filename = stream.title + '.mp3'
    stream.download(output_path, filename)

def download_songs():
    with Executor() as executor:
        executor.map(download_song, playlist.video_urls)

if __name__ == '__main__':
    if os.path.exists(output_path): 
        shutil.rmtree(output_path)
d    download_songs()