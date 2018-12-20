```
echo "# week2_day4" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/timebird7/week2_day4.git
git push -u origin master
```

## 파라미터 

url 뒤에  ?파라미터명=파라미터값  붙여줌



## 웹툰 모아보기

```python
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

```



## 부동산

아파트별로 코드가 있음

http://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do?menuGubun=A&p_apt_code=20121605&p_house_cd=1&p_acc_year=2018&areaCode=&priceCode=



http://rt.molit.go.kr/new/gis/getDanjiComboAjax.do;jsessionid=4FDB92F0D0BE32AE594BE8E9758B8825



p_apt_code=20121605

### 속여야됨

| Host    | rt.molit.go.kr                                               |
| ------- | :----------------------------------------------------------- |
| Referer | http://rt.molit.go.kr/new/gis/srh.do?menuGubun=A&gubunCode=LAND |



bldg_nm

jibun_name

실거래가sum_amt

실거래일deal_dd

실거래월deal_mm

전용면적bldg_area



## 환경변수

누가 보면 안되는 값들 저장

```python
vi ~/.bashrc

# o눌러서 한줄추가
# export TELEGRAM_TOKEN=키값
# :wq로 저장후 종료

source ~/.bashrc
echo $TELEGRAM_TOKEN
#키값이 나오면 성공
```



### 텔레그램 봇

```python
import requests
import json
import os

token = os.getenv('TELEGRAM_TOKEN')

url = 'https://api.hphk.io/telegram/bot{}/getUpdates'.format(token)

response = json.loads(requests.get(url).text)
print(response)

url = 'https://api.hphk.io/telegram/bot{}/sendMessage'.format(token)
chat_id = response["result"][-1]["message"]["from"]["id"]
msg = response["result"][-1]["message"]["text"]

requests.get(url, params = {"chat_id": chat_id, "text": msg})
```



봇에 보낸 메세지를 다시 돌려보내줌



## 크론탭???



## webhook

```python
from flask import Flask, request
import requests
import json
import time
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_URL = "https://api.hphk.io/telegram"

@app.route('/{}'.format(os.getenv('TELEGRAM_TOKEN')), methods=['POST'])
def telegram():
    #텔레그램으로부터 요청이 들어올 경우, 해당 요청을 처리하는 코드
    url = 'https://api.hphk.io/telegram/bot{}/getUpdates'.format(TELEGRAM_TOKEN)
    req = request.get_json()
    chat_id = req["message"]["from"]["id"]
    
    msg = req["message"]["text"]
    
    if msg == "안녕":
        msg = "반말"
    
    
    url = 'https://api.hphk.io/telegram/bot{}/sendMessage'.format(TELEGRAM_TOKEN)
    requests.get(url, params = {"chat_id": chat_id, "text": msg})
    
    
    return '', 200

@app.route('/set_webhook')
def set_webhook():
    url = TELEGRAM_URL + '/bot' + TELEGRAM_TOKEN + '/setWebhook'
    params = {
        'url' : 'https://ssafy-timebird7.c9users.io/{}'.format(TELEGRAM_TOKEN)
    }
    response = requests.get(url, params = params).text  
    print(response)
    
    return response
```

