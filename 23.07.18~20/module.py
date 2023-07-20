from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from urllib.error import HTTPError
import pandas as pd

def date_check(url):
    dummy_list = []
    bsObject = BeautifulSoup(urlopen(url), "html.parser")
    for dates in bsObject.find_all('td', class_="date"):
        date = dates.text.strip()
        dummy_list.append(date)
    return dummy_list

def next_check(url):
    txt_list = []
    bsObject = BeautifulSoup(urlopen(url), "html.parser")
    for txts in bsObject.find_all('a', class_="next-btn disabled"):
        txt = txts.text.strip()
        txt_list.append(txt)
    return txt_list

def page_cnt(url):                                              # 페이지 개수
    li_list = []
    bsObject = BeautifulSoup(urlopen(url), "html.parser")
    list_items = bsObject.select('ul#paging li')
    for li in list_items:
        li_ = li.text
        li_list.append(li_)
    return li_list

def cont_cnt(url):                                                  # 게시물 개수
    soup = BeautifulSoup(urlopen(url), 'html.parser')
    td_tags = soup.find_all('td', class_='tit')
    return len(td_tags)


def extract_data(url):
    bsObject = BeautifulSoup(urlopen(url), "html.parser")

    date_list = []
    title_list = []

    for dates in bsObject.find_all('div', attrs={"class": "articleDate"}):
        date = dates.text.strip()
        date_list.append(date)

    for titles in bsObject.find_all('div', attrs={"class": "articleTitle"}):
        title = titles.text.strip()
        title_list.append(title)

    content_divs = bsObject.find_all('div', attrs={"id": "powerbbsContent"})
    if len(content_divs) > 0:
        content = content_divs[0].text.strip()

    reaction = ' '.join(title_list) + ' ' + (content if len(content_divs) > 0 else '')

    return date_list[0], reaction

def insert_data(df_, date_, reac):
    data = [date_, reac]
    df_.loc[len(df_)] = data

def curr_page(url):
    pattern = r"p=(\d+)"
    match = re.search(pattern, url)
    if match is not None:
        return match.group(1)
    else:
        return 1
    


def mk_df(start, end):

    df = pd.DataFrame(columns=['Date', 'Reaction'])

    for i in range(start, end):
        url = f"https://www.inven.co.kr/board/maple/5974/{i}"

        try:
            html = urlopen(url)
            bsObject = BeautifulSoup(html, "html.parser")

            for dates in bsObject.find_all('div', attrs={"class":"articleDate"}):
                date = dates.text.strip()

            for titles in bsObject.find_all('div', attrs={"class":"articleTitle"}):
                title = titles.text.strip()

            content_divs = bsObject.find_all('div', attrs={"id": "powerbbsContent"})
            if len(content_divs) > 0:
                content = content_divs[0].text.strip()

            reaction = title + ' ' + content

            insert_data(df, date, reaction)

            print(len(df))

            if i % 10 == 0:
                print(f"{i}번째 url 크롤링 완료")

        except HTTPError as e:
            if e.code == 404:
                print(f'HTTP Error 404: The page was not found - URL: {url}')
            else:
                print(f'HTTP Error {e.code}: {e.reason}')

    return df
