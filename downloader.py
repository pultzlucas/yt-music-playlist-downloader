from pytube import Playlist
from termcolor import colored

playlist_url = str(input('Playlist url: '))
output_path = str(input('Output path: '))
playlist = Playlist(playlist_url)

print('Number of videos in playlist: %s' % len(playlist.video_urls))
print('Downloading playlist: ' + playlist.title)

for video in playlist.videos:
    audio = video.streams.filter(only_audio=True).first()
    print(colored('Downloading ', 'green') + audio.title)
    audio.download(output_path, audio.title + '.wav')