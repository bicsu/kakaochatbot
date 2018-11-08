from flask import Flask, jsonify, request, render_template
from sqlalchemy.sql.expression import func
import random
import requests, json
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///movie'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/keyboard')
def keyboard():
    keyboard = {
    "type" : "buttons",
    "buttons" : ["메뉴", "로또", "고양이", "영화", "영화저장"]
    }
    return jsonify(keyboard)

@app.route('/message', methods = ["POST"])
def message():
    user_msg = request.json['content']
    print(user_msg)
    msg = "아직;;"
    img_bool = False
    photo =""
    url = "기본 주소"
    
    if user_msg == "메뉴" :
        # 메뉴를 담은 리스트 만들기
        # 그 중 하나를 랜덤하게 고르기
        # msg변수에 담기
        menus = ["양식", "중식", "일식", "한식", "먹지마"]
        pick = random.choice(menus)
        msg = pick
    elif user_msg == "로또":
        nums = random.sample(range(1,46), 6)
        nums = [str(i) for i in nums]
        msg = ",".join(sorted(nums))
    
    elif user_msg == "고양이":
        img_bool = True
        cat_api = 'https://api.thecatapi.com/v1/images/search?size=full&mime_types=jpg'
        req = requests.get(cat_api).json()
        cat_url = req[0]['url']
        url = cat_url
        msg = "나만 고양이 없어 :("
        
    elif user_msg == "영화":
        img_bool = True
        Movie.query.delete()
        naver_movie = 'https://movie.naver.com/movie/running/current.nhn#'
        
        req = requests.get(naver_movie).text
        soup = BeautifulSoup(req, "html.parser")
        # title = soup.select_one('#content > div.article > div:nth-of-type(1) > div.lst_wrap > ul > li:nth-of-type(1) > dl > dt > a')
        title_list = soup.select('dt.tit > a')
        #star_list = soup.select('a > span.num')
        thumb_list = soup.select('div.star_t1 > a')
        img_url_list = soup.select('div.thumb > a > img')
        
        # movies = {}
        # for i in range(0, 5):
        #     movies[i] = {
        #         'title' : title_list[i].text,
        #         'star' : thumb_list[i].text[0:4],
        #         'url' : img_url_list[i]['src']
                
        #     }
        for i in range(0, 5):
            movie = Movie(title_list[i].text, thumb_list[i].text[0:4], img_url_list[i]['src'])
            db.session.add(movie)
            db.session.commit()
        msg = "저장완료"
        movier = Movie.query.order_by(func.random()).first()
        msg = movier.title + ' / ' + str(movier.star)
        url = movier.img
#    elif user_msg == "영화저장":

        
        
        
    return_dict = {
     'message':{
         'text':msg
        },
     'keyboard':{
        "type" : "buttons",
        "buttons" : ["로또", "메뉴", "고양이", "영화", "영화저장"]
        }
    }
    
    return_img_dict = {
     'message':{
         'text':msg,
         'photo':{
                  "url": url,
                  "width": 720,
                  "height": 630
                 }
                },
     'keyboard':{
        "type" : "buttons",
        "buttons" : ["로또", "메뉴", "고양이", "영화", "영화저장"]
                }
                }
    if img_bool:
        return jsonify(return_img_dict)
    else :
        return jsonify(return_dict)