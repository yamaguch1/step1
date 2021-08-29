#途中
import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import datetime
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager


LOG_FILE_PATH = "./log1/log_{datetime}.log"
EXP_CSV_PATH="./exp_list_{search_keyword}_{datetime}.csv"
log_file_path=LOG_FILE_PATH.format(datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

#ユーザーエージェントといわれるもので、ブラウザの種類やバージョンをサイトに通知するためのもの
HEADER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"

### Chromeを起動する関数
def set_driver(is_headless: bool=False):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if is_headless == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(ChromeDriverManager().install(), options=options)


### ログファイルおよびコンソール出力
def log(txt):
    now=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = '[%s: %s] %s' % ('log1',now , txt)
    # ログ出力
    with open(log_file_path, 'a', encoding='utf-8_sig') as f:
        f.write(logStr + '\n')
    print(logStr)

def find_table_target_word(th_elms, td_elms, target:str):
    # tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm,td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text

### main処理
def main():
    driver = set_driver()
    driver.get("https://www.sbisec.co.jp/ETGate/?_ControlID=WPLEThmR001Control&_PageID=DefaultPID&_DataStoreID=DSWPLEThmR001Control&_ActionID=DefaultAID&getFlg=on")
    driver.find_element_by_id("top_stock_sec").send_keys("アフリカ")
    driver.find_element_by_css_selector("[title='株価検索']").click()
    time.sleep(5)

    name_elms = driver.find_elements_by_css_selector(".accTbl01 tr td:nth-child(1) p:first-child")
    price_elms = driver.find_elements_by_css_selector(".accTbl01 tr td:nth-child(3) p")
    df = pd.DataFrame()
    for name_elm, price_elm in zip(name_elms, price_elms):
        df = df.append({
            "銘柄名": name_elm.text,
            "現在値": price_elm.text.replace(",", "")
        }, ignore_index=True)
    
    df.to_csv("export.csv", encoding="utf-8_sig")
    
    # ページ終了まで繰り返し取得
    exp_name_list = []
    exp_copy_list = []
    exp_status_list = []
    exp_first_year_fee_list = []
    count = 0
    success = 0
    fail = 0
    while True:
        # 検索結果の一番上の会社名を取得(まれに１行目が広告の場合、おかしな動作をするためcassetteRecruit__headingで広告を除外している)
        name_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .cassetteRecruit__name")
        copy_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .cassetteRecruit__copy")
        status_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .labelEmploymentStatus")
        table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition") # 初年度年収
        
        # 1ページ分繰り返し
        for name, copy, status, table in zip(name_list, copy_list, status_list,table_list):
            try:
                # try~exceptはエラーの可能性が高い箇所に配置
                exp_name_list.append(name.text)
                exp_copy_list.append(copy.text)
                exp_status_list.append(status.text)
                # 初年度年収をtableから探す
                first_year_fee = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "初年度年収")
                exp_first_year_fee_list.append(first_year_fee)
                log(f"{count}件目成功 : {name.text}")
                success+=1
            except Exception as e:
                log(f"{count}件目失敗 : {name.text}")
                log(e)
                fail+=1
            finally:
                # finallyは成功でもエラーでも必ず実行
                count+=1
    
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()