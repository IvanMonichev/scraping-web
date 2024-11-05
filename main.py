import ssl
from urllib import request, parse
from bs4 import BeautifulSoup

from config import BASE_URL, COUNT_ARTICLES, SEARCH_WORD
from database import Database


# Отключаем проверку SSL (для учебных целей)
def get_disabled_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    return ctx


def get_page(url):
    ctx = get_disabled_ctx()
    html = request.urlopen(url, context=ctx)
    page = BeautifulSoup(html.read(), 'html.parser')
    return page


def get_articles(search_word, count_articles=1):
    # Encoding russian characters for url
    encoded_search_term = parse.quote(search_word)

    articles = []

    while len(articles) < count_articles:

        number_page = 1
        url_string = f"{BASE_URL}/ru/search/page{number_page}/?q={encoded_search_term}"
        page = get_page(url_string)

        if page is None:
            print(f"The page content could not be retrieved {url_string}")
            break

        found_articles = page.find_all("article", class_="tm-articles-list__item")

        for article in found_articles:
            if len(articles) == count_articles:
                break
            try:
                title_tag = article.find("h2", class_="tm-title tm-title_h2")
                link_tag = title_tag.find("a", class_="tm-title__link")
                author_tag = article.find("a", class_="tm-user-info__username")
                description_tag = article.find("div", class_="article-formatted-body")
                time_tag = article.find("time")

                title = title_tag.get_text(strip=True)
                description = description_tag.get_text(strip=True)
                link = f"{BASE_URL}{link_tag['href']}" if link_tag else "#"
                author = author_tag.get_text(strip=True)
                author_profile_url = f"{BASE_URL}{author_tag['href']}"
                time = time_tag['datetime']

                articles.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "datetime_published": time,
                    "author": {
                        "author": author,
                        "author_profile_url": author_profile_url
                    }
                })
            except Exception as e:
                print(f"Error processing the article: {e}")
            number_page += 1

    return articles


def main():
    articles = get_articles(SEARCH_WORD, COUNT_ARTICLES)
    db = Database()
    db.create_table()
    db.insert_articles(articles)
    db.close()
    print(f"Done! {len(articles)} articles have been successfully recorded.")


# Запускаем main, если скрипт выполнен напрямую
if __name__ == "__main__":
    main()
