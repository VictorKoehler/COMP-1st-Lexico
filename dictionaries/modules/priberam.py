from dictionaries.dict_base import DicionarioBase, firstOrNone, lambdaOrNone
import re

class Priberam(DicionarioBase):
    def __init__(self, *args, **kwargs):
        super().__init__({'palavra', 'classe', 'raiz', 'tempo'}, *args, **kwargs)

    def soup(self, w, *args, **kwargs):
        return self._soup('https://dicionario.priberam.org/' + w)

    def get(self, w, *args, **kwargs):
        s = self.soup(w)
        r = {'palavra': w}
        r['classe'] = r['raiz'] = r['tempo'] = None
        tempo_words = [('pret.', 'p'), ('fut.', 'f'), ('pres.', 't')]

        def get_wclass(i, kwargs):
            if 'sourceinv' in kwargs:
                for j in i.text.lower().split(' '):
                    if kwargs['sourceinv'].conversions.get(j, j) in kwargs['sourceinv'].classes:
                        return j
            return i.text.split(' ')[0].lower()

        try:
            assert len(s.find_all(class_='pb-nomargin-desktop')) == 1
            s.find(class_='pb-nomargin-desktop').decompose()

            classe_raw = s.find_all('categoria_ext_aao')
            classe = [i for i in classe_raw if i.parent.parent.parent.parent.find('b').text.lower().replace('·', '') == w.lower()]
            if not classe:
                classe = classe_raw
            classe = [get_wclass(i, kwargs) for i in classe]
            
            resultsbox = s.find(id='resultados').div.div
            if 'substantivo' in classe and 'verbo' in classe and 'pl.' in str(resultsbox.text):
                r['classe'] = 'substantivo'
                r['raiz'] = lambdaOrNone(resultsbox.find(text=re.compile(r'pl\.')), lambda d: d.parent.a['href'].split('/')[-1])
            else:
                r['classe'] = classe[0] if classe else None
                r['raiz'] = lambdaOrNone(s.find('a', text=re.compile(r'Conjugar')), lambda d: d['href'].split('/')[-1])
                r['tempo'] = self._dirty_tense(resultsbox.text, mapwords=tempo_words)
        except:
            pass
        return r
