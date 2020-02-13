
import urllib
import requests
from bs4 import BeautifulSoup



session = requests.session()
session.headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) \
            Gecko/20100101 Firefox/10.0'
    }
)

params = urllib.parse.urlencode(
    {'q': 'アンジェ・カトリーナ', 'tbm': 'isch', 'ijn': '1'})
query = "https://www.google.co.jp/search" + '?' + params

print(query)

html = session.get(query)
# bs = BeautifulSoup(html.text, 'lxml')
bs = BeautifulSoup(html.text, 'html.parser')
print(bs)




