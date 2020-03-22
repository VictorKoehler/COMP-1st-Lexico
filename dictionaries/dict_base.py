import sys
from . import scrapper

DicionarioChaves = {'palavra', 'classe', 'raiz'}

def firstOrNone(l):
    return l[0] if l else None

def lambdaOrNone(l, f):
    return f(l) if l else None

class DicionarioBase():
    def __init__(self, keys):
        if keys != DicionarioChaves:
            print('Aviso: Chaves inconsistentes em {} ({})'.format(self, keys), file=sys.stderr)
    
    def _soup(self, url, *args, **kwargs):
        return scrapper.request_soup(url, *args, **kwargs)
    
    def soup(self, w, *args, **kwargs):
        return None

    def get(self, w, *args, **kwargs):
        return None
    
