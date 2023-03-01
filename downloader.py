from pytube import Playlist, YouTube
from termcolor import colored
from tqdm import tqdm

playlist_url = 'https://www.youtube.com/playlist?list=PLV1qTAR8p8pjrZNExeqzI8b1fA08tbLpg'#str(input('Playlist url: '))
output_path = 'o'#str(input('Output path: '))
playlist = Playlist(playlist_url)

print('Number of videos in playlist: %s' % len(playlist.video_urls))
print(colored('Downloading playlist: ', 'yellow') + playlist.title)


for video_url in playlist.video_urls:
    def progress_callback(stream, data_chunk: bytes, bytes_remaining: int):
        pbar.update(len(data_chunk))
        
    video = YouTube(video_url, on_progress_callback=progress_callback)
    print(colored('Downloading ', 'green') + video.title)
    
    # stream = video.streams.get_highest_resolution()
    stream = video.streams.get_audio_only()
    pbar = tqdm(total=stream.filesize, unit="bytes", ascii=' >=')
    stream.download(output_path, stream.title + '.mp3')
    pbar.close()
