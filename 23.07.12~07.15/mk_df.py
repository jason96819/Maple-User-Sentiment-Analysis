from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import time
import pandas as pd
import module as m

start = time.time()

url = "https://www.inven.co.kr/board/maple/5974"


options = Options()
options.add_argument('--start-maximized')
options.add_argument('--headless=new')
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)

driver.get(url)
print("0.1")
time.sleep(1)
print("0.2")
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, '#new-board > div.board-bottom > form > select').click()
time.sleep(1)
print("0.3")
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, '#new-board > div.board-bottom > form > select > option:nth-child(5)').click()
time.sleep(1)
print("0.4")
time.sleep(1)
driver.find_element(By.ID, 'sword').send_keys('6차')
time.sleep(1)
print("0.5")
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, '#new-board > div.board-bottom > form > button').click()
time.sleep(1)
print("0.6")
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, '#new-board > div.board-bottom > div > button').click()
time.sleep(1)
print("0.7")
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, '#paging > li:nth-child(12) > a').click()
time.sleep(1)
print("0.8")
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, '#paging > li:nth-child(12) > a').click()
time.sleep(1)

df = pd.DataFrame(columns=['Date', 'Reaction'])

while True:
    url = driver.current_url
    content_cnt = int(m.cont_cnt(url))                          # 게시물 개수
    page_cnt = m.page_cnt(url)                                  # 페이지 개수
    dummy_list = m.date_check(url)
    cur_page = m.curr_page(url)

    print("====================시작=========================")
    print("====================정보=========================")
    print("현재 url :",url)
    print("현재 게시물 개수 :",content_cnt)
    print("현재 페이지 목록 :",page_cnt)
    print("현재 페이지 :",cur_page)

    if '05-30' in dummy_list or '05-29' in dummy_list or '05-28' in dummy_list or '05-27' in dummy_list:
        print("현재 페이지에 특정 str이 있습니다.")
        break
    else:
        print("현재 페이지에 특정 str이 없습니다.")
        print("=================================================")
        if content_cnt == 72:                                   # 첫 페이지
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, '#new-board > form > div > table > tbody > tr:nth-child(3) > td.tit > div > div > a').click()
            time.sleep(1)
            url = driver.current_url
            time.sleep(1)
            date_, reac = m.extract_data(url)
            time.sleep(1)
            m.insert_data(df, date_, reac)
            time.sleep(1)
            print("3번 게시물 크롤링 완료")
            time.sleep(1)
            url = driver.current_url
            content_cnt = int(m.cont_cnt(url))
            for i in range(2, content_cnt+1):                   # 2 ~ content_cnt
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, f'#new-board > form > div > table > tbody > tr:nth-child({i}) > td.tit > div > div > a').click()
                time.sleep(1)
                url = driver.current_url
                time.sleep(1)
                date_, reac = m.extract_data(url)
                time.sleep(1)
                m.insert_data(df, date_, reac)
                time.sleep(1)
                print(f"{i}번 게시물 크롤링 완료")
                url = driver.current_url
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, '#paging > li:nth-child(3) > a').click()
            print("----------페이지 클릭 = 2----------")
            time.sleep(1)
            url = driver.current_url
        else:
            num = m.curr_page(url)
            if num in ["2"]:
                for i in range(4, len(page_cnt)+1):
                    if i == len(page_cnt):
                        url = driver.current_url
                        content_cnt = int(m.cont_cnt(url))
                        for j in range(1, content_cnt+1):               # 1 ~ content_cnt
                            time.sleep(1)
                            driver.find_element(By.CSS_SELECTOR, f'#new-board > form > div > table > tbody > tr:nth-child({j}) > td.tit > div > div > a').click()
                            time.sleep(1)
                            url = driver.current_url
                            time.sleep(1)
                            date_, reac = m.extract_data(url)
                            time.sleep(1)
                            m.insert_data(df, date_, reac)
                            time.sleep(1)
                            print(f"{j}번 게시물 크롤링 완료")
                            url = driver.current_url
                        try:
                            time.sleep(1)
                            driver.find_element(By.CSS_SELECTOR, f'#paging > li:nth-child({i}) > a').click()
                            time.sleep(1)
                            print("----------페이지 클릭 =",i-1, " 다음 클릭이 됩니다.----------")
                            url = driver.current_url
                        except:
                            time.sleep(1)
                            driver.find_element(By.CSS_SELECTOR, '#new-board > div.board-bottom > div > button').click()
                            time.sleep(1)
                            print("----------페이지 클릭 =",i-1, " 다음 클릭이 안됩니다. 다음 검색을 클릭합니다.----------")
                            url = driver.current_url
                    else:
                        url = driver.current_url
                        content_cnt = int(m.cont_cnt(url))
                        for j in range(1, content_cnt+1):       # 1 ~ content_cnt
                            time.sleep(1)
                            driver.find_element(By.CSS_SELECTOR, f'#new-board > form > div > table > tbody > tr:nth-child({j}) > td.tit > div > div > a').click()
                            time.sleep(1)
                            url = driver.current_url
                            time.sleep(1)
                            date_, reac = m.extract_data(url)
                            time.sleep(1)
                            m.insert_data(df, date_, reac)
                            time.sleep(1)
                            print(f"{j}번 게시물 크롤링 완료")
                            url = driver.current_url
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, f'#paging > li:nth-child({i}) > a').click()
                        time.sleep(1)
                        print(f"----------페이지 클릭 = {i-1}----------")
                        url = driver.current_url
                time.sleep(1)
            else:
                for i in range(3, len(page_cnt)+1):
                    if i == len(page_cnt):
                        url = driver.current_url
                        content_cnt = int(m.cont_cnt(url))
                        for j in range(1, content_cnt+1):         # 1 ~ content_cnt
                            time.sleep(1)
                            driver.find_element(By.CSS_SELECTOR, f'#new-board > form > div > table > tbody > tr:nth-child({j}) > td.tit > div > div > a').click()
                            time.sleep(1)
                            url = driver.current_url
                            time.sleep(1)
                            date_, reac = m.extract_data(url)
                            time.sleep(1)
                            m.insert_data(df, date_, reac)
                            time.sleep(1)
                            print(f"{j}번 게시물 크롤링 완료")
                            url = driver.current_url
                        try:
                            time.sleep(1)
                            driver.find_element(By.CSS_SELECTOR, f'#paging > li:nth-child({i}) > a').click()
                            time.sleep(1)
                            print("----------페이지 클릭 =",i-1, " 다음 클릭이 됩니다.----------")
                            url = driver.current_url
                        except:
                            time.sleep(1)
                            driver.find_element(By.CSS_SELECTOR, '#new-board > div.board-bottom > div > button').click()
                            time.sleep(1)
                            print("----------페이지 클릭 =",i-1, " 다음 클릭이 안됩니다. 다음 검색을 클릭합니다.----------")
                            url = driver.current_url
                    else:
                        url = driver.current_url
                        content_cnt = int(m.cont_cnt(url))
                        for j in range(1, content_cnt+1):       # 1 ~ content_cnt
                            time.sleep(1)
                            driver.find_element(By.CSS_SELECTOR, f'#new-board > form > div > table > tbody > tr:nth-child({j}) > td.tit > div > div > a').click()
                            time.sleep(1)
                            url = driver.current_url
                            time.sleep(1)
                            date_, reac = m.extract_data(url)
                            time.sleep(1)
                            m.insert_data(df, date_, reac)
                            time.sleep(1)
                            print(f"{j}번 게시물 크롤링 완료")
                            url = driver.current_url
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, f'#paging > li:nth-child({i}) > a').click()
                        time.sleep(1)
                        print(f"----------페이지 클릭 = {i-1}----------")
                        url = driver.current_url
                time.sleep(1)


end = time.time()


print("====******====종료======*******=======종료=====*******=====종료=======*****============")
print("걸린 시간 :",end-start)

filename = r'C:\Users\user\Documents\nexon\maple_inven_reaction(0601-0713).csv'  # 저장할 파일 경로와 이름 지정
df.to_csv(filename, index=False)                                                 # 데이터프레임을 CSV 파일로 저장
