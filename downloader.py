from pytube import Playlist, YouTube
from termcolor import colored
from tqdm import tqdm
import moviepy.editor as mp
from concurrent.futures.process import ProcessPoolExecutor as Executor
import os
import shutil

playlist_url = 'https://www.youtube.com/playlist?list=PLV1qTAR8p8pjrZNExeqzI8b1fA08tbLpg' # str(input('Playlist url: '))
output_path = 'o'  # str(input('Output path: '))
playlist = Playlist(playlist_url)

print('Number of videos in playlist: %s' % len(playlist.video_urls))
print(colored('Downloading playlist: ', 'yellow') + playlist.title)

def download_song(video_url):
    video = YouTube(video_url)
    print(colored('Downloading ', 'green') + video.title)

    stream = video.streams.get_highest_resolution()

    filename = f'{stream.title}.mp4'
    stream.download(output_path, filename)

    clip = mp.VideoFileClip(f'{output_path}/{filename}')
    clip.audio.write_audiofile(f'{output_path}/{stream.title}.mp3', logger=None)

    os.remove(os.path.realpath(f'./{output_path}/{filename}'))
    # print('*'*20)
    # print(os.path.realpath(f'./{output_path}/{filename}'))
    # print('*'*20)

if __name__ == '__main__':
    if os.path.exists('o'): shutil.rmtree('o')
    with Executor() as executor:
        executor.map(download_song, playlist.video_urls)
    videos = [f for f in os.listdir(output_path) if os.path.isfile(os.path.join(output_path, f)) and os.path.splitext(f)[-1] == '.mp4']
    for video in videos: 
        os.remove(output_path + '/' + video)
