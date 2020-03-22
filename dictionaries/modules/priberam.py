from dictionaries.dict_base import DicionarioBase, firstOrNone, lambdaOrNone
import re

class Priberam(DicionarioBase):
    def __init__(self, *args, **kwargs):
        super().__init__({'palavra', 'classe', 'raiz'}, *args, **kwargs)

    def soup(self, w, *args, **kwargs):
        return self._soup('https://dicionario.priberam.org/' + w)

    def get(self, w, *args, **kwargs):
        s = self.soup(w)
        r = {'palavra': w}
        r['classe'] = r['raiz'] = None
        try:
            assert len(s.find_all(class_='pb-nomargin-desktop')) == 1
            s.find(class_='pb-nomargin-desktop').decompose()
            classe = [i.text.split(' ')[0].lower() for i in s.find_all('categoria_ext_aao')]
            resultsbox = s.find(id='resultados').div.div
            if 'substantivo' in classe and 'pl.' in resultsbox.text:
                r['classe'] = 'substantivo'
                r['raiz'] = lambdaOrNone(resultsbox.find(text=re.compile(r'pl\.')), lambda d: d.parent.a['href'].split('/')[-1])
            else:
                r['classe'] = classe[0] if classe else None
                r['raiz'] = lambdaOrNone(s.find('a', text=re.compile(r'Conjugar')), lambda d: d['href'].split('/')[-1])
        except:
            pass
        return r
