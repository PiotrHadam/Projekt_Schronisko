from bs4 import BeautifulSoup
from urllib.request import urlopen
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
        y.append(float(stats_a[i][1]))

    fig = plt.figure()
    plt.bar(x,y, color="#d6a984")

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
        y.append(float(stats_s[i][1]))

    fig = plt.figure()
    plt.bar(x,y, color="#d6a984")

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data

def names_graph():
    names = {}
    for a in get_animals():
        if a.name[:1] not in names.keys():
            names[a.name[:1]] = 0
        names[a.name[:1]] += 1

    fig = plt.figure()
    plt.bar(names.keys(), names.values(), color="#d6a984")

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
    def __init__(self, logo="", address="", social="", title=""):
        self.logo = logo
        self.address = address
        self.social = social
        self.title = title

def get_contact():
    panels = []
    with urlopen('https://www.psitulmnie.pl/kontakt.php') as response:
            soup = BeautifulSoup(response, 'html.parser')
            for x in soup.select('.panel .panel-body'):
                panels.append(x)

    contact = Contact()

    for i in panels[2]:
        contact.logo = "https://www.psitulmnie.pl" + panels[2].find('img').get('src')

        titles = panels[2].find_all('b')
        contact.title = titles[0].get_text()
        #address = titles[1].get_text()

        if panels[2].find('img') != i:

            for word in str(i).split():
                if word == ' Zabrze':
                    break
                else:
                    contact.title += word

                    
            contact.address += str(i)
            
    return contact