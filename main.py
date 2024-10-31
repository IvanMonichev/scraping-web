import ssl
from urllib import request, parse

from bs4 import BeautifulSoup

# Constants
BASE_URL = "https://habr.com"
SEARCH_PATH = "/ru/search/"
QUERY_PARAM = "q"
SEARCH_TERM = "микросервисы"
TARGET_TYPE_PARAM = "target_type"
TARGET_TYPE_VALUE = "posts"
ORDER_PARAM = "order"
ORDER_VALUE = "relevance"

encoded_search_term = parse.quote(SEARCH_TERM)

URL_STRING = f"{BASE_URL}{SEARCH_PATH}?{QUERY_PARAM}={encoded_search_term}&{TARGET_TYPE_PARAM}={TARGET_TYPE_VALUE}&{ORDER_PARAM}={ORDER_VALUE}"

# Disable SSL for learning task
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

html = request.urlopen(URL_STRING, context=ctx)
bs = BeautifulSoup(html.read(), 'html.parser')

titles = bs.find_all("h2", class_="tm-title tm-title_h2")
for title in titles:
    print(title.get_text(strip=True))
