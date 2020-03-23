import sys
from . import scrapper

DicionarioChaves = {'palavra', 'classe', 'raiz', 'tempo'}

def firstOrNone(l):
    return l[0] if l else None

def lambdaOrNone(l, f):
    return f(l) if l else None

def firstMatch(it, func, default=None):
    for i in it:
        if func(i):
            return i
    return default

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
    
    def _dirty_tense(self, desc_txt, defaultNone=None, mapwords=None):
        tempo_words = mapwords or [('pretérito', 'p'), ('passado', 'p'), ('futuro', 'f'), ('particípio', 'p')]
        tempo_map = {'p': 'passado', 'f': 'futuro', 't': 'presente'}
        if desc_txt is None:
            return defaultNone
        desc_txt = str(desc_txt).lower()
        tt = firstMatch(tempo_words, lambda i: i[0] in desc_txt, ('', 't'))
        return tempo_map[tt[1]]
