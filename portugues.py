import lexico
from sys import stderr, argv
from dictionaries import *

try:
    from tqdm import tqdm
except:
    print('You can install tqdm to better view progress...', file=stderr)
    tqdm = lambda l: l

dictman = DictionaryManager()
def dictman_adapter(orig):
    try:
        for i in tqdm(orig):
            i['tempo'] = ''
            if i['state'] == 'palavra':
                i['state'] = dictman.get(i['token'], 'classe')
                if i['state'] == 'verbo': # Stemiza apenas verbos
                    i['tempo'] = dictman.get(i['token'], 'tempo', optional='')
                    i['token'] = dictman.get(i['token'], 'raiz', optional=i['token'])
    finally:
        dictman.save()
    return orig

if __name__ == "__main__":
    if not '-n' in argv:
        p0 = lexico.main_module(dictman_adapter, doprint=False)
        for i in p0:
            if (not '--stop-word' in argv) and i['state'] in ['artigo', 'conjunção', 'preposição']:
                continue
            print('{}|{}|{}|{}'.format(lexico.token_repr(i['token']), i['state'], i['linecounter'], i['tempo']))
