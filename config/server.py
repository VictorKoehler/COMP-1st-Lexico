from http.server import HTTPServer, SimpleHTTPRequestHandler
from base64 import b64decode

class HTTPPostHandler(SimpleHTTPRequestHandler):
    def do_GET(self, *args, **kwargs):
        patt = 'fsm.json?setdata='
        rl = self.requestline
        if patt in rl:
            dtit = rl[rl.find(patt) + len(patt):].split(' ')[0]
            dt = b64decode(dtit).decode()
            with open('fsm.json', 'w') as f:
                f.write(dt)
                print("Configuration file changed.")
        return super().do_GET(*args, **kwargs)

def run(server_class=HTTPServer, handler_class=HTTPPostHandler, port=8000):
    '''Um simples servidor HTTP que possibilita a atualização do arquivo fsm.json.
    '''
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    port = 8000
    print('http://127.0.0.1:{}'.format(port))
    run(port=port)
