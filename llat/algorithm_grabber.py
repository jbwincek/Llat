from bs4 import BeautifulSoup as bs
from bs4 import NavigableString
import json
import requests
import re
import pprint
#import argparse

url = "http://algdb.net/Set/PLL"

r = requests.get(url)
soup = bs(r.text, 'html.parser')

we_want = (1, )

output = {} 
for row in soup.find_all('tbody')[0].contents:
    if not isinstance(row, NavigableString):
        algs = []
        for alg in row.contents[5].contents:
            try:
                raw = alg.strip()
                if raw:
                    algs.append(raw)
            except TypeError:
                pass
        output[row.contents[1].a.text] = algs

with open('PLL_algs.json', 'w') as f:
    f.write(json.dumps(output))
    print('written')