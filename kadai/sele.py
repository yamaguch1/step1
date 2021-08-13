
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import csv


def set_driver():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # ChromeのWebDriverオブジェクトを作成する。
    driver = webdriver.Chrome(options=options, executable_path = "C:\\Users\\81904\\Desktop\\Mypandas\\chromedriver.exe")
    driver.implicitly_wait(3)
    return driver

# main処理
def main():
    search_keyword = input("検索ワードを入力: ")

    driver = set_driver()
    driver.implicitly_wait(3)

    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(2)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(2)

    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    time.sleep(3)

    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(3)

    # 検索結果の一番上の会社名を取得
    name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
    jobdescription_list = driver.find_elements_by_class_name("tableCondition__body")
    annualincome_list = driver.find_elements_by_class_name("tableCondition__body")
    name_list = name_list[0:5]
    jobdescription_list = jobdescription_list[0:5]
    annualincome_list = annualincome_list[0:5]

    # 空のDataFrame作成
    df = pd.DataFrame()

    # 1ページ分繰り返し
    print(f"{len(name_list)}件")
    for name in name_list:
        print(name.text)
    for jobdescription in jobdescription_list:
        print(jobdescription.text)
    for annualincome in annualincome_list:
        print(annualincome.text)

    # DataFrameに対して辞書形式でデータを追加する
    for n in range(5):
        df = df.append(
            {"会社名": name_list[n].text, 
            "仕事内容": jobdescription_list[n].text,
            "初年度年収": annualincome_list[n].text
            }, ignore_index=True)

    
    HEADER = ['会社名', '仕事内容', '初年度年収'] 
    with open('job.csv', 'w', encoding='utf-8_sig') as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
            
        row = [df]
        writer.writerow(row)
    
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
