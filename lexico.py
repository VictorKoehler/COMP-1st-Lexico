from fsm_reader import read_fsm
import re
from sys import argv

def char_matches_rule(rule: str, charac: str):
    '''Dado uma regra e um caractere, determina se o caractere satisfaz a regra (retorna True).
    A regra será interpretada usando a implementação padrão de procura de Regex do Python em duas situações:
    1) rule possui o padrão 'regex(...)'
    2) rule possui o padrão '[...]
    Do contrário, existem duas possíveis condições:
    Se rule começa com 1 ou 3 contra-barras (isto é: '\...' ou '\\\...'), então será realizada uma simples busca invertida.
    Senão, será realizada uma simples busca em rule por charac (isto é: charac in rule).
    '''
    magicregexword = 'regex('
    shallregex = rule[0] == '[' and rule[-1] == ']'

    if rule.startswith(magicregexword):
        rule = rule[len(magicregexword):-1]
        shallregex = True

    if shallregex:
        return not re.match(rule, charac) is None
    elif (rule[0] == '\\' and rule[1] != '\\') or (rule.startswith('\\\\\\') and rule[3] != '\\'):
        return not charac in rule
    else:
        return charac in rule


def get_matches_links(links, charac):
    return [(n, r) for n, r in links if char_matches_rule(r, charac)]

def parse_input_fsm(fsm: list, fsm_start: int, reserved: list, inp: str):
    def decide_token_label(cfg, fsm, reserved):
        sttxt = fsm[cfg['state']]['text']
        if sttxt == 'identificador' and cfg['token'] in reserved:
            return 'reservado'
        return sttxt

    inp += '\n'
    last_valid_cfg = {
        'linecounter': 1,
        'linebegin': 0,
        'poscounter': 0,
        'posbegin': 0,
        'state': fsm_start,
        'token': None
    }
    current_cfg = last_valid_cfg
    seqr = []
    while current_cfg['poscounter'] < len(inp):
        posc = current_cfg['poscounter']
        c = inp[posc]
        state = fsm[current_cfg['state']]
        out = get_matches_links(state['links'], c)

        if c == '\n':
            current_cfg['linecounter'] += 1
            current_cfg['linebegin'] = posc

        if len(out) == 0: # Não há saídas: Ou é um caractere inválido ou um token é terminado.
            if current_cfg['state'] == fsm_start:
                raise Exception("Invalid character at line {}, pos {}: {}".format(current_cfg['linecounter'], posc - current_cfg['linebegin'], c))
            last_valid_cfg['token'] = inp[last_valid_cfg['posbegin']:last_valid_cfg['poscounter']+1]
            last_valid_cfg['state'] = decide_token_label(last_valid_cfg, fsm, reserved)
            seqr.append(last_valid_cfg.copy())

            # Continua de onde não parou
            current_cfg = last_valid_cfg
            current_cfg['state'] = fsm_start
            current_cfg['poscounter'] += 1

        elif len(out) == 1: # Uma saída, (salva?) e altera para o estado.
            if current_cfg['state'] == fsm_start:
                current_cfg['posbegin'] = posc
            current_cfg['state'] = out[0][0]
            if fsm[current_cfg['state']]['accept']:
                last_valid_cfg = current_cfg.copy()
            current_cfg['poscounter'] += 1
        else: # Assertiva: Deu ruim! Ambiguidade no modelo
            raise Exception("Ambiguous FSM")

    
    return seqr

def beauty_print(results):
    def print_line(t, s, l, c=' '):
        def str_spaced(s, n=10):
            return "'" + s + "'" + (n-len(s))*c
        print('{}|{}|{}'.format(str_spaced(t, 15), str_spaced(s, 20), str_spaced(str(l), 5)))
    bb = {
        'atribuicao': 'Atribuição',
        'delimitador': 'Delimitador',
        'identificador': 'Identificador',
        'inteiro': 'Número inteiro',
        'reservado': 'Palavra reservada',
        'real': 'Número Real'
    }
    print_line('TOKEN', 'CLASSIFICAÇÂO', 'LINHA', '-')
    for i in results:
        print_line(i['token'], bb.get(i['state'], i['state']), i['linecounter'])

if __name__ == "__main__":
    fsm, fsm_start, reserved = read_fsm()
    inp = argv[1] if len(argv) >= 2 else input()
    with open(inp, 'r') as f:
        inp = f.read()
    p0 = parse_input_fsm(fsm, fsm_start, reserved, inp)
    beauty_print(p0)