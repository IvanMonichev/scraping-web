import ssl
from urllib import request, parse

# Constants
BASE_URL = "https://habr.com"
SEARCH_PATH = "/ru/search/"
QUERY_PARAM = "q"
SEARCH_TERM = "микросервисы"
TARGET_TYPE_PARAM = "target_type"
TARGET_TYPE_VALUE = "posts"
ORDER_PARAM = "order"
ORDER_VALUE = "relevance"

# Кодирование поискового запроса
encoded_search_term = parse.quote(SEARCH_TERM)

# Собираем URL
URL_STRING = f"{BASE_URL}{SEARCH_PATH}?{QUERY_PARAM}={encoded_search_term}&{TARGET_TYPE_PARAM}={TARGET_TYPE_VALUE}&{ORDER_PARAM}={ORDER_VALUE}"


# Отключение проверки сертификатов для учебных целей
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

html = request.urlopen(URL_STRING, context=ctx)
print(html.read().decode('utf-8'))