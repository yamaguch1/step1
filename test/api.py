import urllib.request
import json


with urllib.request.urlopen('https://www.jma.go.jp/bosai/forecast/data/overview_forecast/130000.json?__time__=202102240506') as response:
    html = response.read().decode("utf-8")
    print(html)

    
html = open('test.json', 'r')
json_dict = json.load(html)
print('json_dict:{}'.format(type(json_dict)))

menu = json_dict["menu"]