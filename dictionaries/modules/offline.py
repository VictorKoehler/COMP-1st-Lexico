from dictionaries.dict_base import DicionarioBase, firstOrNone, lambdaOrNone
import re

offline_dict = dict()

class Offline(DicionarioBase):
    def __init__(self, *args, **kwargs):
        super().__init__({'palavra', 'classe', 'raiz'}, *args, **kwargs)

    def get(self, w, *args, **kwargs):
        return offline_dict.get(w.lower(), {})

def reg(w, classe, raiz=None):
    if w in offline_dict:
        raise Exception('Palavra repetida!')
    w = w.lower()
    r = {'palavra': w}
    r['classe'] = classe
    r['raiz'] = raiz or w
    offline_dict[w] = r

reg('A', 'artigo')
reg('As', 'artigo', 'A')
reg('O', 'artigo')
reg('Os', 'artigo', 'O')

reg('e', 'conjunção')
reg('mas', 'conjunção')
reg('ou', 'conjunção')
reg('logo', 'conjunção')
reg('pois', 'conjunção')
reg('que', 'conjunção')
reg('como', 'conjunção')
reg('porque', 'conjunção')

reg('ante', 'preposição')
reg('após', 'preposição')
reg('até', 'preposição')
reg('com', 'preposição')
reg('contra', 'preposição')
reg('de', 'preposição')
reg('desde', 'preposição')
reg('em', 'preposição')
reg('entre', 'preposição')
reg('para', 'preposição')
reg('pra', 'preposição')
reg('per', 'preposição')
reg('perante', 'preposição')
reg('por', 'preposição')
reg('sem', 'preposição')
reg('sob', 'preposição')
reg('sobre', 'preposição')
reg('trás', 'preposição')

reg('da',  'preposição') # Contração
reg('do',  'preposição') # Contração
reg('das', 'preposição', 'da') # Contração
reg('dos', 'preposição', 'do') # Contração

reg('são', 'verbo', 'ser')