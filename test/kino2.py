from pandas_datareader import data 
import pandas as pd                
import matplotlib.pyplot as plt    
import numpy as np                 
# %matplotlib inlnen
#pd.core.common.is_list_like = pd.api.types.is_list_like

start = '2019-06-01' 
end = '2020-06-01'   

df = data.DataReader('^N225','yahoo',start,end)   

df.head(10) 

# df.dtypes

df.index 
date = df.index 
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

#棒グラフの描画（matplotlibで可視化） 
plt.figure(figsize=(30,15))
plt.bar(date,df['Volume'],label='Volume',color='grey')
plt.legend()

#線グラフと棒グラフを同じグラフの中で２分割
plt.figure(figsize=(30,15))
plt.subplot(2,1,1) #分割表示のsubplot 縦方向、横方向、グラフを配置する位置のインデックス
plt.plot(date,price,label='Close',color='#99b898') 
plt.plot(date,df['sma01'],label='sma01',color='e84a5f')
plt.plot(date,df['sma02'],label='sma02',color='#ff847c')
plt.plot(date,df['sma03'],label='sma03',color='#feceab')
plt.legend()

plt.subplot(2,1,2)
plt.bar(date,df['Volume'],label='Volume',color='grey')
plt.legend()

#日本企業の個別銘柄の株のデータ取得
#まず東京証券取引所のページにアクセス
#例：リクルートホールディングスで検索→コード「6098」コピー
company_code = '6098.jp'
#df = data.DataReader('6098','stooq') #ポーランドのサイトを使ってデータ取得（コード,データソース）
df = data.DataReader(company_code,'stooq') 
df.head()
df.index.min()
df.index.max()
df.index.max()
df.head()
df.tail()
df = df.sort_index() #dfの変数を並び替えして更新（通常のカラムの並びを変える際はsort_valuesデータフレームの要素の並び替え）
df.head(10)
#df.index>='2019-06-01 00:00:00'
