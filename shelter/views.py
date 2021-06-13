from django.shortcuts import render
from django.http import HttpResponse
from .functions import *

def home_page(request):
    return render(request, 'shelter/welcome.html', {})

def gallery(request):
    animals = get_animals()
    return render(request, 'shelter/gallery.html', {'animals_list': animals})

def stats_page(request):
    stats_a, stats_s = get_stats()
    graph_a = animals_graph()
    graph_s = sizes_graph()
    return render(request, 'shelter/stats.html', {'stats_a': stats_a, 'stats_s': stats_s, 'graph_a': graph_a, 'graph_s': graph_s})