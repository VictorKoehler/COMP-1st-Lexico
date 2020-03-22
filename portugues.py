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
    for i in tqdm(orig):
        if i['state'] == 'palavra':
            i['state'] = dictman.get(i['token'], 'classe')
            if i['state'] == 'verbo': # Stemiza apenas verbos
                i['token'] = dictman.get(i['token'], 'raiz', optional=i['token'])
    dictman.save()
    return orig

if __name__ == "__main__":
    if not '-n' in argv:
        lexico.main_module(dictman_adapter)
