from dictionaries.dict_base import DicionarioBase, firstOrNone, lambdaOrNone
import re

class LexicoPT(DicionarioBase):
    def __init__(self, *args, **kwargs):
        super().__init__({'palavra', 'classe', 'raiz'}, *args, **kwargs)

    def soup(self, w, *args, **kwargs):
        return self._soup('https://www.lexico.pt/' + w)

    def get(self, w, *args, **kwargs):
        s = self.soup(w)
        r = {'palavra': w}
        classe_map = {'subst.' : 'substantivo', 'adj.': 'adjetivo', 'pron.': 'pronome', 'v.': 'verbo', 'prep.': 'preposição'}
        r['classe'] = r['raiz'] = None
        try:
            classe = re.split(re.compile(r'\n *\n'), '\n'.join(s.find(id='significado').strings))
            classe = [i.split('\n')[0].strip().split(' ')[0].strip() for i in classe]
            classe = [classe_map[i] for i in classe if i in classe_map]
            r['classe'] = classe[0] if classe else None
            if r['classe'] == 'verbo':
                r['raiz'] = lambdaOrNone(s.find(id='significado').find('strong'), lambda d: d.text)
        except:
            pass
        return r
