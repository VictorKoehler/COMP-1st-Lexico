from dictionaries.dict_base import DicionarioBase, firstOrNone, lambdaOrNone
import re

class Dicio(DicionarioBase):
    def __init__(self, *args, **kwargs):
        super().__init__({'palavra', 'classe', 'raiz', 'tempo'}, *args, **kwargs)
    
    def soup(self, w, *args, **kwargs):
        return self._soup('https://www.dicio.com.br/' + w.lower())

    def get(self, w, *args, **kwargs):
        s = self.soup(w)
        r = {'palavra': w.lower()}
        ll = s.find(text=re.compile(r'Flexão do verbo'))
        r['classe'] = lambdaOrNone(s.find(class_='cl'), lambda d: d.text.strip().split(' ')[0])
        if r['classe'] is None and ll:
            r['classe'] = 'verbo'
        r['raiz'] = lambdaOrNone(ll, lambda d: d.parent.a.text)
        r['tempo'] = None
        if r['classe'] == 'verbo':
            r['tempo'] = self._dirty_tense(lambdaOrNone(ll, lambda d: d.parent.text), 'presente')
        return r
