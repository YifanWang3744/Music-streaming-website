from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import random
from random import randint


base_url = "https://www.last.fm"

def get_soup(url):
    url = Request(url, headers={'User-Agent': 'Chrome/99'})
    page = urlopen(url)
    html = page.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# s = get_soup(base_url)
# print(s.prettify())

global_album_id = 1

def get_genre_data(url):
    global global_album_id
    cards = get_soup(url).find_all('li', class_="resource-list--release-list-item-wrap")
    data = []
    for card in cards:
        album = card.find("h3").find("a")
        artist = card.find("p", class_="resource-list--release-list-item-artist").find("a")
        album_url = base_url + album['href']
        artist_url = base_url + artist['href']
        album_name = album.get_text()
        artist_name = artist.get_text()
        album_id = global_album_id
        global_album_id += 1

        data.append({
            "album_name": album_name,
            "album_url": album_url,
            "artist_name": artist_name,
            "artist_url": artist_url,
            "album_id": album_id
        })
    print((data))

    return data


song_counter = 1
def get_album_data(url):
    soup = get_soup(url)
    
    data = {}
    global song_counter

    # Get songs
    song_list = soup.findAll("td", class_="chartlist-name")
    
    # Get sng release date
    date_data = soup.findAll("dt", class_="catalogue-metadata-heading")
    for d in range(len(date_data)):
        if(date_data[d].get_text()=='Release Date'):
            date = date_data[d].next_sibling.next_sibling.get_text()
            break
    
    # Get songs details
    data["song_list"] = []
    for song in song_list:
        s = {
            "sid": str(song_counter),
            "song_name": song.get_text().strip('\n'),
        }
        song_counter += 1
        data["song_list"].append(s)


    data["release_date"] = date
    print(data)

    return data
s = get_album_data("https://www.last.fm/music/Nirvana/Nevermind")

def get_artist_data(url):
    soup = get_soup(url)
    divs = soup.findAll("div", class_="readmore")
    # Get rid
    data = {"aid": soup.find("span", class_="copy_shortcut_code").get_text()[2:-1]}
    # Get bio
    bio = divs[0].get_text().strip().split(".")
    data["bio"] = bio[0]
    if len(data["bio"]) >= 200:
        data["bio"] = data["bio"][:200]

    # Get members
    members = divs[1].findAll("a")
    data["members"] = []
    counter = 1
    for member in members:
        name = member.get_text().split()
        creator = {"cid": data["aid"] + str(counter), "f_name": name[0], "l_name": name[-1]}
        data["members"].append(creator)
        counter += 1

    return data


def get_label_data():
    records_labels = [{"label_name":'Virgin Records', "lid":'1'},{"label_name":'Island Records', "lid":'2'},{"label_name":'Warner Music Group', "lid":'3'},{"label_name":'Red Hill Records', "lid":'4'},
                        {"label_name":'Universal Music Publishing Group', "lid":'5'},{"label_name":'Sony Music Entertainment', "lid":'6'}]
    return random.choice(records_labels)
