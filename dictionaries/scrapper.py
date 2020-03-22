from bs4 import BeautifulSoup
import requests
import os

def import_headers(f='headers'):
    with open(os.path.join(os.path.dirname(__file__), f), 'r') as fh:
        return dict(l.strip().split(': ', maxsplit=1) for l in fh.readlines())

try:
    hheaders = headers
except:
    headers = import_headers()

def request_soup(u, h=headers):
    return BeautifulSoup(requests.get(u, headers=h).content, 'html5lib')

