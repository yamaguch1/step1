import openpyxl #py -m pip install openpyxlでインストール
import pandas as pd #CSVファイルやExcelファイルを読み取るための機能や、データを表やグラフにする機能など。Series（１列）DateFrame（２列）
import glob #特定の条件が位置するファイル名を取得することができます


import_file_path = '' #ファイルのパスを入力 「ファイルを読み込む場所」という変数
exsel_sheet_name = '' #シート名を格納 編集したいシート名
export_file_path = ''#ファイルの分割したファイルを置く場所という変数


