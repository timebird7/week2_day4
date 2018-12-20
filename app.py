from flask import Flask, render_template, request
import requests
import time
import json
from bs4 import BeautifulSoup as bs


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/toon')
def toon():
    cat = request.args.get('type')
    if(cat == 'naver'):
        today = time.strftime("%a").lower()
        print(today)
    # 네이버 웹툰을 가져올 수 있는 주소url을 파악한다.
    # url 변수에 저장한다.
    # 해당 주소로 요청을 보내 정보를 가져온다.
    # 받은 정보를 bs를 이용해 검색하기 좋게 만든다
    # 네이버 웹툰 페이지로 가서, 내가 원하는 정보가 어디에 있는지 파악한다.

        url = 'https://comic.naver.com/webtoon/weekdayList.nhn?week=' + today
        response = requests.get(url).text
        soup = bs(response, 'html.parser')

        toons = []
        li = soup.select('.img_list li')
        for item in li:
            toon = {
            'title' : item.select_one('dt a').text,
            'url' : "https://comic.naver.com/" + item.select('dt a')[0]['href'],
            'img_url' : item.select('.thumb img')[0]['src']
            }
        
            toons.append(toon)
    elif(cat == 'daum'):
        today = time.strftime("%a").lower()

# 내가 원하는 정보를 얻을 수 있는 주소를 url이라고 하는 변수에 담는다.
# 해당 url에 요청을 보내 응답을 받아 저장한다.
# python으로 어떻게 json을 파싱(딕셔너리 형으로 전환) 구글링
# 내가 원하는 데이터를 꺼내서 조합한다.

        url = 'http://webtoon.daum.net/data/pc/webtoon/list_serialized/' + today
        response = requests.get(url).text
        document = json.loads(response)
        data = document['data']
        toons = []
        for toon in data:
            toon = {
            'title' : toon['title'],
            'url' : 'http://webtoon.daum.net/webtoon/view/{}'.format(toon['nickname']),
            'img_url' : toon['pcThumbnailImage']['url']
            }
            
            toons.append(toon)
    
    return render_template("toon.html", cat = cat, t = toons)

@app.route('/apart')
def apart():
    #1. 내가 원하는 정보를 얻을 수 있는 url을 url변수에 저장한다.
    #1-1. request header에 추가할 정보를 dictionary 형태로 저장한다
    headers = {
        "Host" : "rt.molit.go.kr",
        "Referer" : "http://rt.molit.go.kr/new/gis/srh.do?menuGubun=A&gubunCode=LAND"
    }
    url = 'http://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do?menuGubun=A&p_apt_code=20121605&p_house_cd=1&p_acc_year=2018&areaCode=&priceCode='
    #2. request 의 get 기능을 이용하여 해당 url에 header와 함께 요청을 보낸다.
    response = requests.get(url, headers = headers).text
    #3. 응답으로 온 코드의 형태를 살펴본다.(json/xml/html)
    document = json.loads(response)
    
    for d in document["result"]:
        print(d["BLDG_NM"])
    print(document)
    return render_template("apart.html")

@app.route('/exchange')
def exchange():
    url = 'https://finance.naver.com/marketindex/?tabSel=exchange#tab_section'
    
    response = requests.get(url).text
    soup = bs(response, 'html.parser')
    moneys = []
    li = soup.select('.selectbox-default option')
    for item in li:
        money = {
        'title' : item.select_one('option').text,
        'price' : item.select('option.value')["value"].text
        }
        print(money)
    return render_template("exchange.html")
