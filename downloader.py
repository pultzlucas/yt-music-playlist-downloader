from pytube import Playlist, YouTube
from termcolor import colored
from tqdm import tqdm
import moviepy.editor as mp
from concurrent.futures.process import ProcessPoolExecutor as Executor
import os
import shutil


# str(input('Playlist url: '))
playlist_url = 'https://www.youtube.com/playlist?list=PLV1qTAR8p8piVBzQncqjR7srgXuyUeQYU'
output_path = 'o'  # str(input('Output path: '))
playlist = Playlist(playlist_url)

print('Number of videos in playlist: %s' % len(playlist.video_urls))
print(colored('Downloading playlist: ', 'yellow') + playlist.title)


# def progress_callback(arg, data_chunk: bytes, arg2):
#     pbar.update(len(data_chunk))


# def completed_callback(stream, arg2):
#     print(arg2)
#     clip = mp.VideoFileClip(
#         output_path + '/' + stream.title + '.mp4').subclip(0, 20)
#     clip.audio.write_audiofile(output_path + '/' + stream.title + ".mp3")


def download_song(video_url):
    video = YouTube(video_url)
    print(colored('Downloading ', 'green') + video.title)

    stream = video.streams.get_highest_resolution()

    filename = stream.title + '.mp4'
    stream.download(output_path, filename)

    clip = mp.VideoFileClip(output_path + '/' + filename)
    clip.audio.write_audiofile(output_path + '/' + stream.title + '.mp3')

if __name__ == '__main__':
    if os.path.exists('o'): shutil.rmtree('o')
    with Executor() as executor:
        executor.map(download_song, playlist.video_urls)
    videos = [f for f in os.listdir(output_path) if os.path.isfile(os.path.join(output_path, f)) and os.path.splitext(f)[-1] == '.mp4']
    for video in videos: 
        os.remove(output_path + '/' + video)
