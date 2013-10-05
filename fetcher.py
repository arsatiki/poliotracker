import requests
import hashlib

SOURCE = 'http://www.polioeradication.org/Dataandmonitoring/Poliothisweek.aspx'

def fetch():
    r = requests.get(SOURCE)
    f = open('checksum', 'r+')
    s_old = f.read(20)
    s_new = hashlib.sha1(r.content).digest()
    f.seek(0)
    f.write(s_new)
    f.close()
    
    return r.text, s_new != s_old

if __name__ == '__main__':
    text, modified = fetch()
    print modified