from flask import Flask, jsonify, request, render_template
import requests
import requests_cache
import json

app = Flask(__name__)

news_api_key = "eb02151432cc49cda4fbfabef9b4890a"
domain = "https://newsapi.org/v2/"
country = "tr"

#requests_cache.install_cache()

def get_headlines(country):
    global domain
    global news_api_key
    url = '%stop-headlines?country=%s&apiKey=%s'%(domain,country,news_api_key)
    response = requests.get(url)
    Jresponse = response.text
    news = json.loads(Jresponse)
    return news['articles']

def get_news(param):
    global domain
    global news_api_key
    url = '%severything?q=%s&apiKey=%s'%(domain,param,news_api_key)
    response = requests.get(url)
    Jresponse = response.text
    news = json.loads(Jresponse)
    return news['articles']

@app.route("/api/ping",methods=["GET"])
def pinging():
    response = {"succes":"true"}
    return jsonify(response)

@app.route("/")
def home():
    return render_template("home.html", title="Daily News")

@app.route("/about")
def about():
    return render_template("about.html",title="About")

@app.route("/headlines",methods=["GET"])
def headlines():
    country_list = {
        'Australia':'au','Austria':'at','Belgium':'be','Brazil':'br','Italy':'it',
        'Japan':'jp','United Kingdom':'gb','United States':'us',
        'Turkey':'tr','France':'fr','Germany':'de'
        }

    if request.args:
        country = request.args['country']
        news = get_headlines(country)
        for key,value in country_list.items():
            if value == country:
                title = "Headlines for " + key
    else:
        news = ""
        title = "Headlines"


    return render_template("headlines.html", news=news, country_list=country_list, title=title)

@app.route("/city",methods=["GET"])
def city():
    data = get_news("city")
    return render_template("city.html", news=data, title="City")

@app.route("/woman",methods=["GET"])
def women():
    data = get_news("woman")
    return render_template("woman.html", news=data, title="Woman")

if __name__ == "__main__":
    app.run(debug=True)
