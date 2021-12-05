from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import re
from time import sleep


# Create your views here.
def index(request):
    all_articles = []
    for page_number in range(1, 51):
        page_url = "https://habr.com/ru/news/page" + str(page_number)
        r = requests.get(page_url)
        c = r.content
        soup = BeautifulSoup(c, 'html.parser')
        articles = soup.find_all("article", {"class": "tm-articles-list__item"})
        for article in articles:
            art = {}
            art['article_url'] = "https://habr.com" + \
                                 article.find("a", {"class": "tm-article-snippet__title-link"}).get("href")
            art['title'] = article.find("a", {"class": "tm-article-snippet__title-link"}).span.get_text()
            art['time'] = article.find("span", {"class": "tm-article-snippet__datetime-published"}).time.get("title")
            art['score'] = article.find("span", {"class": "tm-votes-meter__value"}).get_text()
            art['views'] = article.find("span", {"class": "tm-icon-counter__value"}).get_text()
            art['comments'] = article.find("span",
                                           {"class": "tm-article-comments-counter-link__value"}).get_text().strip()
            art['score'] = int(art['score'].replace("+", "").replace("–", "-"))
            art['comments'] = int(art['comments'])
            try:
                votes = re.findall(r'↑\d+|↓\d+',
                                   article.find("span", {"class": "tm-votes-meter__value_rating"}).get('title'))
                art['controversy'] = min(int(votes[0][1:]), int(votes[1][1:]))
                art['votes'] = votes[0] + ' ' + votes[1]
            except:
                art['votes'] = '↑0 ↓0'
                art['controversy'] = 0
            all_articles.append(art)
        sleep(10)

    all_articles.sort(key=lambda d: d['comments'], reverse=True)

    return render(request, "index.html", {'news': all_articles})
