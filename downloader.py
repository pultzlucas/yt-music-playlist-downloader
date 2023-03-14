from pytube import Playlist, YouTube
from termcolor import colored
from concurrent.futures.process import ProcessPoolExecutor as Executor
import os
import shutil
import eyed3
from eyed3.id3.frames import ImageFrame
import requests
from PIL import Image

# str(input('Playlist url: '))
playlist_url = 'https://music.youtube.com/playlist?list=PLV1qTAR8p8phZ2kv0LyTvbZwb2XUNEQ5K'
output_path = 'o'  # str(input('Output path: '))
playlist = Playlist(playlist_url)

print('Number of videos in playlist: %s' % len(playlist.video_urls))
print(colored('Downloading playlist: ', 'yellow') + playlist.title)

def add_tags_to_audio_file():
    pass

def download_video_thumbnail(video_title, thumb_url):
    img_data = requests.get(thumb_url).content
    if not os.path.exists('Thumbs'): os.mkdir('Thumbs')
    path = f'./Thumbs/{video_title}.jpg'
    with open(path, 'wb') as handler:
        handler.write(img_data)
    # foo = Image.open(path)
    # foo = foo.resize((100, 200), Image.ANTIALIAS)
    # foo.save(path, optimize=True, quality=95)
    # print(foo.size)
    return path

def download_song(video_url):
    video = YouTube(video_url)
    stream = video.streams.get_audio_only()

    print(colored('Downloading ', 'green') + stream.title)

    filename = stream.title + '.mp3'

    thumb_path = download_video_thumbnail(stream.title, video.thumbnail_url)
    stream.download(output_path, filename)

    audio = eyed3.load(output_path + '/' + filename)
    
    # if audio == None:
    #     print(os.path.exists('./' + output_path + '/' + filename), './' + output_path + '/' + filename)
    #     print(stream.title)

    if not audio == None:
        audio.initTag()
        audio.tag.title = u'' + stream.title
        audio.tag.album = u'' + playlist.title
        audio.tag.images.set(3, open(thumb_path, 'rb').read(), 'image/jpeg')
        audio.tag.save(version=eyed3.id3.ID3_V2_3)


if __name__ == '__main__':
    if os.path.exists(output_path): shutil.rmtree(output_path)
    if os.path.exists('Thumbs'): shutil.rmtree('Thumbs')

    # with Executor() as executor:
        # executor.map(download_song, playlist.video_urls)
    for song in playlist.video_urls:
        download_song(song)