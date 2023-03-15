from pytube import Playlist, YouTube
from termcolor import colored
from concurrent.futures.process import ProcessPoolExecutor as Executor
import os
import shutil
from eyed3 import id3
import requests
import eyed3

playlist_url = None
playlist = None
output_folder_path = 'Output'

def add_tags_to_audio_file():
    pass

def download_video_thumbnail(video_title, thumb_url):
    img_data = requests.get(thumb_url).content
    if not os.path.exists('Thumbs'): os.mkdir('Thumbs')
    path = f'./Thumbs/{video_title}.jpg'
    with open(path, 'wb') as handler:
        handler.write(img_data)
    return path

def download_song(video_url):
    video = YouTube(video_url)
    stream = video.streams.get_audio_only()

    print(colored('Downloading ', 'green') + stream.title)

    filename = stream.title + '.mp3'

    thumb_path = download_video_thumbnail(stream.title, video.thumbnail_url)
    stream.download(output_folder_path, filename)

    # Adding Tags to audio file
    tag = id3.Tag()
    tag.parse(output_folder_path + '/' + filename)
    tag.title = u'' + stream.title
    tag.album = u'' + output_folder_path
    tag.artist = u'' + video.author
    tag.images.set(3, open(thumb_path, 'rb').read(), 'image/jpeg')
    tag.save(version=eyed3.id3.ID3_V2_3)


def main():
    # Playlist Example: https://music.youtube.com/playlist?list=PLV1qTAR8p8phZ2kv0LyTvbZwb2XUNEQ5K

    playlist_url = str(input('Playlist url: ')) 
    playlist = Playlist(playlist_url)

    print('Number of videos in playlist: %s' % len(playlist.video_urls))
    print(colored('Downloading playlist: ', 'yellow') + playlist.title)

    if os.path.exists('Thumbs'): shutil.rmtree('Thumbs')
    if os.path.exists(output_folder_path): shutil.rmtree(output_folder_path)

    with Executor() as executor:
        executor.map(download_song, playlist.video_urls)

if __name__ == '__main__':
    main()