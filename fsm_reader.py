import json

def read_fsm_plain(filename='fsm.json'):
    with open(filename, 'r') as f:
        return json.loads(f.read())

def read_reserved_keywords(reservedfile='reserved.txt'):
    with open(reservedfile, 'r') as f:
        return [i.strip() for i in f.readlines()]

def read_fsm(filename='fsm.json', reservedfile='reserved.txt'):
    plain = read_fsm_plain(filename)
    reserved = read_reserved_keywords(reservedfile)
    
    def filter_dict(i: dict, filt: set):
        return { k[1]: i[k[0]] for k in filt }
    def filter_nodes(i: dict):
        nodes_filter = { ('text', 'text'), ('isAcceptState', 'accept') }
        r = filter_dict(i, nodes_filter)
        r['links'] = []
        return r

    nodes = [filter_nodes(i) for i in plain['nodes']]
    for l in plain['links']:
        a = int(l['nodeA' if l['type'] == 'Link' else 'node'])
        b = int(l['nodeB' if l['type'] == 'Link' else 'node'])
        nodes[a]['links'].append((b, l['text']))
    
    start = 0
    for i in range(len(nodes)):
        if nodes[i]['text'] == 'start':
            start = i
            break

    return nodes, start, reserved