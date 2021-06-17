from django.shortcuts import render
from django.http import HttpResponse
from .functions import *

def home_page(request):
    contact = get_contact()
    return render(request, 'shelter/welcome.html', {'logo': contact.logo, 'address': contact.address, 
    'social': contact.social, 'title': contact.title})

def gallery(request):
    animals = get_animals()
    return render(request, 'shelter/gallery.html', {'animals_list': animals})

def stats_page(request):
    stats_a, stats_s = get_stats()
    graph_a = animals_graph()
    graph_s = sizes_graph()
    graph_n = names_graph()
    return render(request, 'shelter/stats.html', {'stats_a': stats_a, 'stats_s': stats_s, 'graph_a': graph_a, 'graph_s': graph_s, 'graph_n': graph_n})

def events_page(request):
    events = get_events()
    return render(request, 'shelter/events.html', {'events': events})
