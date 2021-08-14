import json
import requests

params = {'after': '2018-12-01T00:00:00'}
URL = 'https://www.jma.go.jp/bosai/forecast/data/overview_forecast/130000.json?__time__=202102240506'
print(URL)
response = requests.get(URL, params=params)
print(response.status_code)

if response.status_code == 200:
    # jsonモジュールを使用する例
    data = response.text
    json_data = json.loads(data)
    print(json_data)
    # 実はjsonモジュールを使わなくても、以下の1行でJSONデータを得ることができる
    #json_data = response.json()

    # 各エントリのタイトルを一覧で表示
    for entry in json_data:
        print(entry['title']['rendered'])
