import os 
import hashlib 
import argparse
from urllib import request

parser = argparse.ArgumentParser()
parser.add_argument(
        '-t', '--type', 
        choices=['human', 'wget'], default='human')
parser.add_argument('-a', '--ip', default=None)
args = parser.parse_args()

host = args.ip or os.environ["SERV_IP"]

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
INDEX_FILE = os.path.join(BASE_PATH, 'index.txt')

with open(INDEX_FILE, encoding='utf-8') as fin:
    files = [(name.strip(), md5) 
             for md5, _, name in (l.partition(' ') for l in fin)]

to_download = []

for name, md5 in files:
    path = os.path.join(BASE_PATH, name)
    try:
        hash_md5 = hashlib.md5()
        with open(path, 'rb') as fin:
            for chunk in iter(lambda: fin.read(4096), b""):
                hash_md5.update(chunk)
        if md5 != hash_md5.hexdigest():
            print("updated:", name)
            to_download.append(name)
    except FileNotFoundError:
        print("new:".ljust(len("updated:")), name)
        to_download.append(name)

for name in to_download:
    url = f"ftp://{host}/tda/{name}"
    to  = os.path.join(BASE_PATH, name)
    if args.type == "human":
        print(url, "->", to)
    elif args.type == "wget":
        print(f"wget -O '{to}' {url}")

