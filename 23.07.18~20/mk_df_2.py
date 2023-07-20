import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.error
import urllib.request
from urllib.error import HTTPError
import module as m

df = m.mk_df(1591880, 1845250)                                                #1591880(6/1) ~ 1845249(6/30)


filename = r'C:\Users\user\Documents\nexon\maple_inven_all.csv'               # 저장할 파일 경로와 이름 지정
df.to_csv(filename, index=False)                                              # 데이터프레임을 CSV 파일로 저장
