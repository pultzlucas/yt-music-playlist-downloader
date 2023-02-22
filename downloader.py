from pytube import Playlist
playlist_url = str(input('Playlist url: '))
output_path = str(input('Output path: '))
playlist = Playlist(playlist_url)

print('Downloading playlist: ' + playlist.title)
print('Number of videos in playlist: %s' % len(playlist.video_urls))

for video in playlist.videos:
    audio = video.streams.filter(only_audio=True).first()
    print('Downloading -> ' + audio.title)
    audio.download(output_path, audio.title + '.wav')