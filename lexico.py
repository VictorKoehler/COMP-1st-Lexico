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
    '''Dado uma lista de regras e um caractere, retorna todas as regras a qual o caractere se aplica.
    '''
    return [(n, r) for n, r in links if char_matches_rule(r, charac)]

def parse_input_fsm(fsm: list, fsm_start: int, reserved: list, inp: str):
    '''Dado uma FSM, seu estado inicial, uma lista de palavras reservadas e uma string de entrada, retorna a análise lexica da entrada.
    O retorno é uma lista de dicionários.
    Cada dicionário contém:
        o 'token',
        o estado/classificação 'state',
        a linha de ocorrência 'linecounter',
        a posição relativa ao ínicio da linha 'poslinebegin',
        a posição absoluta no arquivo 'posbegin',
        a posição absoluta do término do token no arquivo 'poscounter'.
    '''

    def decide_token_label(cfg, fsm, reserved):
        '''Dá um nome/classificação apresentável ao token.
        '''
        sttxt = fsm[cfg['state']]['text']
        if sttxt == 'identificador' and cfg['token'] in reserved:
            return 'reservado'
        return sttxt

    # Variáveis locais
    # current_cfg contém a configuração da máquina. (posição do cursor, estado, contadores, etc)
    # last_valid_cfg contém a última configuração válida da máquina.
    # Sempre que precisarmos, voltamos ao passado usando last_valid_cfg.
    last_valid_cfg = {
        'linecounter': 1,
        'poslinebegin': 0,
        'poscounter': 0,
        'posbegin': 0,
        'state': fsm_start,
        'token': None
    }
    current_cfg = last_valid_cfg
    seqr = [] # Retorno
    inp += '\n' # Garante o término da leitura da máquina.

    # Enquanto não chegamos no fim do arquivo, interpretamos-o com a FSM
    while current_cfg['poscounter'] < len(inp):

        posc = current_cfg['poscounter'] # Cursor da string
        c = inp[posc] # Caractere
        state = fsm[current_cfg['state']] # Estado da máquina
        out = get_matches_links(state['links'], c) # No atual estado da máquina, onde conseguimos chegar com c?

        if c == '\n': # Incrementa os contadores
            current_cfg['linecounter'] += 1
            current_cfg['poslinebegin'] = posc

        if len(out) == 0: # Não há saídas: Ou é um caractere inválido ou um token é terminado e o cursor é restaurado.
            # Estamos no estado inicial e não há transições para c: Entrada inválida.
            if current_cfg['state'] == fsm_start:
                raise Exception("Invalid character at line {}, pos {}: {}".format(current_cfg['linecounter'], posc - current_cfg['poslinebegin'], c))

            # Se não estamos no estado inicial e mesmo assim não há saída para o cursor, então salvamos o último estado válido.
            # Aqui damos uns toques finais no dicionário.
            last_valid_cfg['token'] = inp[last_valid_cfg['posbegin']:last_valid_cfg['poscounter']+1]
            last_valid_cfg['state'] = decide_token_label(last_valid_cfg, fsm, reserved)
            seqr.append(last_valid_cfg.copy())

            # Restaura a máquina no passado, dizendo que o último estado salvo já virou um token;
            # recomeçamos a máquina no estado inicial e reposicionamos o cursor.
            current_cfg = last_valid_cfg.copy()
            last_valid_cfg['token'] = None
            last_valid_cfg['state'] = None
            current_cfg['state'] = fsm_start
            current_cfg['poscounter'] += 1

        elif len(out) == 1: # Uma saída, (salva?) e altera para o estado.
            # Se o estado atual é o inicial, então dizemos que tudo começou agora, antes de irmos para o próximo estado.
            if current_cfg['state'] == fsm_start:
                current_cfg['posbegin'] = posc

            current_cfg['state'] = out[0][0] # Dizemos que o estado atual = próximo.
            if fsm[current_cfg['state']]['accept']: # Se o estado for de aceitação, então ele é o último válido.
                last_valid_cfg = current_cfg.copy()
            current_cfg['poscounter'] += 1 # Incrementa o cursor.
        
        else: # Assertiva: Deu ruim! Ambiguidade no modelo
            raise Exception("Ambiguous FSM")
    
    if current_cfg['state'] != fsm_start:
        import sys
        print("WARNING: Parsing didn't completed.", file=sys.stderr)
    
    return seqr

def token_repr(t):
    d = {'\t': '\\t', '\n': '\\n', '\r': '\\r', '\f': '\\f', '\v': '\\v'}
    return d.get(t, t)

def beauty_print(results):
    '''Imprime o resultado de parse_input_fsm de forma amigável.
    '''
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
        print_line(token_repr(i['token']), bb.get(i['state'], i['state']), i['linecounter'])


def main_module(lf=lambda i: i, doprint=True):
    '''Por padrão, ou recebe o arquivo de entrada como argumento da linha de comando, ou lê o caminho da entrada padrão.
    '''
    fsm, fsm_start, reserved = read_fsm()
    inp = argv[1] if len(argv) >= 2 else input()
    with open(inp, 'r') as f:
        inp = f.read()
    p0 = lf(parse_input_fsm(fsm, fsm_start, reserved, inp))
    
    if doprint:
        if '-u' in argv:
            for i in p0:
                print('{}|{}|{}'.format(token_repr(i['token']), i['state'], i['linecounter']))
        else:
            beauty_print(p0)
    return p0

if __name__ == "__main__":
    main_module()