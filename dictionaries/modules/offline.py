from dictionaries.dict_base import DicionarioBase, firstOrNone, lambdaOrNone
import re

offline_dict = dict()

class Offline(DicionarioBase):
    def __init__(self, *args, **kwargs):
        super().__init__({'palavra', 'classe', 'raiz', 'tempo'}, *args, **kwargs)

    def get(self, w, *args, **kwargs):
        return offline_dict.get(w.lower(), {})

def reg(w, classe, raiz=None, tempo=None):
    if w in offline_dict:
        raise Exception('Palavra repetida!')
    w = w.lower()
    r = {'palavra': w}
    r['classe'] = classe
    r['raiz'] = raiz or w
    r['tempo'] = tempo
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

reg('são', 'verbo', 'ser', 'presente')
reg('foram', 'verbo', 'ir', 'passado')

reg('eu', 'pronome')
reg('nós', 'pronome')
reg('tu', 'pronome')
reg('você', 'pronome')
reg('vós', 'pronome')
reg('vocês', 'pronome', 'você')
reg('ele', 'pronome')
reg('eles', 'pronome', 'ele')
reg('ela', 'pronome')
reg('elas', 'pronome', 'ela')

reg('patinhos', 'substantivo', 'pato')
reg('patinho', 'substantivo', 'pato')
