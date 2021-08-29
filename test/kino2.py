from pandas_datareader import data #pip install pandas_datareader このライブラリは日経平均株価やナスダック、日本の個別銘柄のデータを取得可能
import pandas as pd                #データ解析を支援、集計や加工など
import matplotlib.pyplot as plt    #パイソンのグラフを書く
import numpy as np                 
%matplotlib inlnen
#pd.core.common.is_list_like = pd.api.types.is_list_like

start = '2019-06-01' #取得する日
end = '2020-06-01'   #取得する最後の日

df = data.DataReader('^N225','yahoo',start,end)   #取得したいティッカーシンボル,とデータソースの名前←これでdfという変数にpandasのデータフレームとして日経平均のデータが格納される
df.head(10) #headで上位10を表示

df.dtypes

df.index #DatetimeIndex時系列データとして扱える可視化にも便利

date = df.index #変数に代入
price = df['Adj Close']

plt.plot(date,price) #線グラフの描画（matplotlibで可視化） 
#X軸にdate,Y軸にprice
plt.figure(figsize=(30,10))
#グラフのサイズが小さいので横の長さ30、縦の長さ10
plt.plot(date,price,label='Nikkei225') #線グラフに名前を付ける＝凡例
plt.title('N225',color='blue',backgroundcolor='white',size=40,loc='center') #タイトルをつける
plt.xlabel('date',color='blue',size=30) #X軸の名前
plt.ylabel('price',color='blue',size=40) #Y軸の名前
plt.legend()#名前を表示させる

#単純移動平均
span01=5 #移動平均の期間（5日間の移動平均）
span02=25
span03=50

df['sma01'] = price.rolling(window=span01).mean() #rollingメソッドで窓関数を適用できる、サンプリングの間隔を指定する
#単純移動平均の略称sma01というカラム名（）内は移動平均の日数、meanは平均（maxは最大値を取得、minは最小値）
df['sma02'] = price.rolling(window=span02).mean()
df['sma03'] = price.rolling(window=span03).mean()

pd.set_option('display.max_rows',None) #行の省略を防ぐ
df.head(100) #上位100

#配色の参考サイトhttp://colorhunt.co/palette/184189
plt.figure(figsize=(30,10))
plt.plot(date,price,label='Nikkei225',color='#99b898') #線グラフに名前を付ける＝凡例
plt.plot(date,df['sma01'],label='sma01',color='e84a5f')
plt.plot(date,df['sma02'],label='sma02',color='#ff847c')
plt.plot(date,df['sma03'],label='sma03',color='#feceab')

plt.title('N225',color='white',backgroundcolor='grey',size=30,loc='center') #タイトルをつける
plt.xlabel('date',color='grey',size=20) #X軸の名前
plt.ylabel('price',color='grey',size=20) #Y軸の名前
plt.legend()#名前を表示させる

#ゴールデンクロス＝短期の移動平均線が中期以上の移動平均線を下から上に抜けること（価格が上昇のサイン）⇔デッドクロス
