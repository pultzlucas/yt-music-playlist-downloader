from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
import os
import shutil

output_dir = 'Lyrics'

def get_lyrics_url(name):
    url = f'https://www.vagalume.com.br/search?q={name}'
    html = requests.get(url).content
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    for a in r.html.find('a'):
        if 'class' in a.attrs and a.attrs['class'][0] == 'gs-title':
            return a.attrs['href']        

def get_lyrics(song_name):
    url = get_lyrics_url(song_name)
    print(url)
    
    return
    lyrics_html = requests.get(url)    
    soup = BeautifulSoup(lyrics_html.content, 'html.parser')
    
    
    # soup = soup.find('div', class_='cnt-letra')
    # soup = soup.find_all('p')
    # paragraphs = []
    # for p in soup:
    #     paragraph = []
    #     for line in str(p)[3:-4].split('<br/>'):
    #         paragraph.append(line)
    #     paragraphs.append('\n'.join(paragraph))
    # return '\n'.join(paragraphs)

def write_lyric_file(song_name, lyrics):
    with open(f'Lyrics/{song_name}.txt', "w", encoding="utf-8") as f:
        f.write(lyrics)
        f.close()
        
def main():
    os.mkdir(output_dir)
    songs = os.listdir('o')
    songs_lyrics = [get_lyrics(song[0:-4]) for song in songs]
    
    
if __name__ == '__main__':
    if os.path.exists(output_dir): shutil.rmtree(output_dir)
    main()
