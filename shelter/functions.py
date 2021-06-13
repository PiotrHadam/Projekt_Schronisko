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