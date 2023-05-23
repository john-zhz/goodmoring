from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ[b'START_DATE']
city = os.environ[b'CITY']
birthday = os.environ[b'BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = [b'oNfo16DOY_7_8a5WDLTH6wS6yh2s',b'oNfo16BBMqTcGqaZSKyS4r1p4dmg']
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res[b'data'][b'list'][0]
  return weather

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()[b'data'][b'text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weather = get_weather()
wea, temperature = weather[b'weather'], math.floor(weather[b'temp'])
data = {
  "weather":{
    "value":wea
  },
  "temperature":{
    "value":temperature
  },
  "love_days":{
    "value":get_count()
  },
  "birthday_left":{
    "value":get_birthday()
  },
  "words":{
    "value":get_words(), 
    "color":get_random_color()
  },
  "city":{
    "value":city
  },
  "highest": {
    "value": math.floor(weather[b'high'])
  },
  "lowest": {
    "value": math.floor(weather[b'low'])
  }
}
print(data)
print(user_id)
for user in user_id:
  print(user)
  res = wm.send_template(user, template_id, data)
  print(res)
