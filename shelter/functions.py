from bs4 import BeautifulSoup
from urllib.request import urlopen
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
from io import StringIO
import numpy as np

class Animal:
    def __init__(self, name="", image="", link=""):
        self.name = name
        self.image = image
        self.link = link

def get_animals():
    animals = []
    with urlopen('https://www.psitulmnie.pl/galeria.php/') as response:
        soup = BeautifulSoup(response, 'html.parser')
        for a in soup.select('.thumbnail'):
            animal = Animal()
            animal.name = a.find('span').get_text()
            animal.image = 'https://www.psitulmnie.pl' + a.find('img').get('src')
            animal.link = 'https://www.psitulmnie.pl/' + a.find('a').get('href')
            animals.append(animal)
    return animals

def get_stats():
    stats = {}
    with urlopen('https://www.psitulmnie.pl/galeria.php/') as response:
        soup = BeautifulSoup(response, 'html.parser')
        for a in soup.select('.table'):
            for i in range (len(a.find_all('td'))//2):
                stats[a.find_all('td')[2*i].get_text()] = a.find_all('td')[2*i+1].get_text()

    stats_a = list(stats.items())[:4]
    stats_s = list(stats.items())[4:]
    return stats_a, stats_s

def animals_graph():
    stats_a = get_stats()[0]
    x = []
    y = []
    for i in range(len(stats_a)):
        x.append(stats_a[i][0])
        y.append(int(stats_a[i][1]))

    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Gill Sans']
    rcParams['font.size'] = 14
        
    fig, ax = plt.subplots(figsize=(10,7))
        
    plt.bar(x, y, color="#d6a984")
    
    for s in ['top','bottom','left','right']:
        ax.spines[s].set_visible(False)
        
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
        
    ax.xaxis.set_tick_params(pad=5)
    ax.yaxis.set_tick_params(pad=5)
    
    ax.grid(b=True, color='grey', linestyle='-.', linewidth=0.5, alpha=0.2)
    
    rects = ax.patches

    for rect, label in zip(rects, y):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label, ha='center', va='bottom')

    ax.set_title('Liczba zwierząt w zależności od rodzaju', pad=10)
    ax.set_xlabel('Rodzaj zwierzaka')
    ax.set_ylabel('Liczba zwierząt')

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data

def sizes_graph():
    stats_s = get_stats()[1]
    x = []
    y = []
    for i in range(len(stats_s)):
        x.append(stats_s[i][0])
        y.append(int(stats_s[i][1]))

    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Gill Sans']
    rcParams['font.size'] = 14
        
    fig, ax = plt.subplots(figsize=(10,7))
        
    plt.bar(x, y, color="#d6a984")
    
    for s in ['top','bottom','left','right']:
        ax.spines[s].set_visible(False)
        
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
        
    ax.xaxis.set_tick_params(pad=5)
    ax.yaxis.set_tick_params(pad=5)
    
    ax.grid(b=True, color='grey', linestyle='-.', linewidth=0.5, alpha=0.2)
    
    rects = ax.patches

    for rect, label in zip(rects, y):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label, ha='center', va='bottom')

    ax.set_title('Liczba zwierząt w zależności od rozmiaru', pad=10)
    ax.set_xlabel('Wielkość')
    ax.set_ylabel('Liczba zwierząt')

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data

def names_graph():
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Gill Sans']
    rcParams['font.size'] = 14
    names = {}
    for a in get_animals():
        if a.name[:1] not in names.keys():
            names[a.name[:1]] = 0
        names[a.name[:1]] += 1
        
    fig, ax = plt.subplots(figsize=(10,7))
        
    plt.bar(names.keys(), names.values(), color="#d6a984")
    
    for s in ['top','bottom','left','right']:
        ax.spines[s].set_visible(False)
        
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
        
    ax.xaxis.set_tick_params(pad=5)
    ax.yaxis.set_tick_params(pad=5)
    
    ax.grid(b=True, color='grey', linestyle='-.', linewidth=0.5, alpha=0.2)
    
    rects = ax.patches

    for rect, label in zip(rects, names.values()):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label, ha='center', va='bottom')

    ax.set_title('Liczba zwierząt w zależności od pierwszej litery imienia', pad=10)
    ax.set_xlabel('Litera')
    ax.set_ylabel('Liczba zwierząt')

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data
        
class Event:
    def __init__(self, event="", link="", content='', htmlID="", tagID=""):
        self.event = event
        self.link = link
        self.content = content
        self.htmlID = htmlID
        self.tagID = tagID
    def __str__(self):
        return f'Wydarzenie {self.event} pod linkiem {self.link}: \n {self.text}'

def get_events():
    events = []
    summary = []
    with urlopen('https://www.psitulmnie.pl/aktualnosci.php') as response:
        soup = BeautifulSoup(response, 'html.parser')
        counter = 0
        for x in soup.select('.col-md-push-3 .panel .panel-body .panel-group .panel'):
            ev = Event()
            counter += 1
            if 'Schroniskowe wiadomości' not in x.find('a').get_text():
                ev.event = x.find('a').get_text()
                ev.link = x.find('a').get('href')
                t = ""
                for i in x.select('.panel-collapse .panel-body'):
                    t += str(i)
                ev.content = t
                ev.htmlID = "id" + str(counter)
                ev.tagID = ev.link[1:]
                events.append(ev)

    return events

class Contact:
    def __init__(self, logo="", address="", email="", title="", facebook1="", facebook2="", hours="", collage=[]):
        self.logo = logo
        self.address = address
        self.email = email
        self.title = title
        self.facebook1 = facebook1
        self.facebook2 = facebook2
        self.hours = hours
        self.collage = collage

def get_contact():
    panels = []
    contact = Contact()

    with urlopen('https://www.psitulmnie.pl/kontakt.php') as response:
            soup = BeautifulSoup(response, 'html.parser')
            for x in soup.select('.panel .panel-body'):
                panels.append(x)

            contact.logo = "https://www.psitulmnie.pl" + soup.find('img', {'class': 'img-responsive'}).get('src')

            nicePhotos = soup.select('img', {'class': 'nicephotos'})

            for i in range(1,6):
                contact.collage.append("https://www.psitulmnie.pl" + nicePhotos[i].get('src'))
            
            


    canContinueAddress = True
    canContinueTitle = True
    canContinueHours = True

    for i in panels[2]:
        #contact.logo = "https://www.psitulmnie.pl" + panels[2].find('img').get('src')

        #titles = panels[2].find_all('b')
        #contact.shelterName = titles[0].get_text()

        #address = titles[1].get_text()

        contact.email = panels[2].find('a').get_text()
        links = [a['href'] for a in panels[2].find_all('a', href=True) if a.text]
        contact.facebook1 = links[1]
        contact.facebook2 = links[2]
        #dojazd = "https://www.psitulmnie.pl" + links[3]
        #formularz = "https://www.psitulmnie.pl" + links[4]


        if panels[2].find('img') != i:

            if str(i)!="<b>Adres schroniska:</b>" and canContinueTitle:
                contact.title += str(i)
            elif str(i)!="Godziny otwarcia:" and canContinueAddress and not canContinueTitle:
                contact.address += str(i)
            elif str(i)=="Godziny otwarcia:":
                canContinueAddress = False
            elif "Email" not in str(i) and canContinueHours and not canContinueAddress and not canContinueTitle:
                contact.hours += str(i)
            elif "Email" in str(i):
                canContinueHours = False
            else:
                canContinueTitle = False
            
            
    return contact