from dictionaries.dict_base import DicionarioBase, firstOrNone, lambdaOrNone
import re

class Dicio(DicionarioBase):
    def __init__(self, *args, **kwargs):
        super().__init__({'palavra', 'classe', 'raiz'}, *args, **kwargs)
    
    def soup(self, w, *args, **kwargs):
        return self._soup('https://www.dicio.com.br/' + w)

    def get(self, w, *args, **kwargs):
        s = self.soup(w)
        r = {'palavra': w}
        r['classe'] = firstOrNone(s.find_all(class_='cl'))
        r['raiz'] = lambdaOrNone(s.find(text=re.compile(r'Flexão do verbo')), lambda d: d.parent.a.text)
        return r
