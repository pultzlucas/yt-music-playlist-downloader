from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests

def get_lyrics_url(name):
    url = f'https://www.letras.mus.br/?q={name}'
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    for a in r.html.find('a'):
        if 'class' in a.attrs and a.attrs['class'][0] == 'gs-title':
            return a.attrs['href']        

link = get_lyrics_url('Me encontra')
response = requests.get(link)

soup = BeautifulSoup(response.content, 'html.parser')
soup = soup.find('div', class_='cnt-letra')
soup = soup.find_all('p')

for p in soup:
    print(p.text)
