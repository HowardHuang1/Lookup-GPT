'''
This program prunes the sublister python script outputs (output.txt) into a new text file (domains.txt)
This program is used to remove duplicates and to smash "www." in front of every domain then prune the domains to check if they are actually up
'''

import requests
from concurrent.futures import ThreadPoolExecutor

domains = set()
with open('output.txt', 'r') as f:
    while True:
        line = f.readline()
        if not line.strip():
            break 
        # remove the www. if there is one
        line = line.replace('www.', '')
        domains.add(line)

# domains with www. slapped on and as a list
domains = ["https://www." + i.replace('\n', '') for i in domains]
# _ is the list of domains that are actually up
_ = []

# now ima try to request all the domains to see if they actually up
def fetch_url(url):
    try:
        r = requests.get(url, timeout=10)
        print(f'Fetching {url}...')
        if r.status_code == 200:
            _.append(url.replace("https://", ''))
    except Exception as e:
        pass

# Use ThreadPoolExecutor for concurrent requests
with ThreadPoolExecutor(max_workers=20) as executor:
    # Submit each URL for concurrent processing
    executor.map(fetch_url, domains)

open('domains.txt', 'w').write('\n'.join(_))