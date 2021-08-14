import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import datetime
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


LOG_FILE_PATH = "./log1/log_{datetime}.log"
EXP_CSV_PATH="./exp_list_{search_keyword}_{datetime}.csv"
log_file_path=LOG_FILE_PATH.format(datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))


### Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ['enable-automation'])


    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
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
def log1(txt):
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
    log1("処理開始")
    search_keyword=input("検索キーワードを入力してください：")
    log1("検索キーワード:{}".format(search_keyword))
    # driverを起動
    driver = set_driver("chromedriver.exe", False)
    # Webサイトを開く
    driver.get("https://site0.sbisec.co.jp/marble/fund/powersearch/fundpsearch.do?")
    time.sleep(5)
    try:
        # ポップアップを閉じる（seleniumだけではクローズできない）
        # driver.execute_script('document.querySelector(".karte-close").click()')
        # time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass

    # 検索窓に入力
    driver.find_element_by_class_name(".fundNameInput").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name(".fundNameSearch .img").click()

    # ページ終了まで繰り返し取得
    exp_name_list = []
    exp_value_list = []
    exp_volume_list = []
    exp_comparison_list = []
    count = 0
    success = 0
    fail = 0
    while True:
        # 検索結果の一番上の会社名を取得(まれに１行目が広告の場合、おかしな動作をするためcassetteRecruit__headingで広告を除外している)
        name_list = driver.find_elements_by_css_selector(".fundDetail_89311199")
        value_list = driver.find_elements_by_css_selector(".tab_values_base .table. tbody .tr:nth-child(1) .td:nth-child(2)")
        volume_list = driver.find_elements_by_css_selector(".tab_values_base .table .tbody. tr:nth-child(1) .td:nth-child(3)")
        comparison_list = driver.find_elements_by_css_selector(".tab_values_base .table .tbody .tr:nth-child(1) .td:nth-child(4)") 
        
        # 1ページ分繰り返し
        for name, value, volume, comparison in zip(name_list, value_list, volume_list,comparison_list):
            try:
                # try~exceptはエラーの可能性が高い箇所に配置
                exp_name_list.append(name.text)
                exp_value_list.append(value.text)
                # 初年度年収をtableから探す
                name = find_table_target_word(name.find_elements_by_tag_name("th"), name.find_elements_by_tag_name("td"), "銘柄名")
                exp_name_list.append(name)
                value = find_table_target_word(value.find_elements_by_tag_name("th"), value.find_elements_by_tag_name("td"), "現在値")
                exp_value_list.append(value)
                volume = find_table_target_word(volume.find_elements_by_tag_name("th"), volume.find_elements_by_tag_name("td"), "出来高")
                exp_volume_list.append(volume)
                comparison = find_table_target_word(comparison.find_elements_by_tag_name("th"), comparison.find_elements_by_tag_name("td"), "前日比")
                exp_comparison_list.append(comparison)

                log1(f"{count}件目成功 : {name}.text")
                success+=1
            except Exception as e:
                log1(f"{count}件目失敗 : {name}.text")
                log1(e)
                fail+=1
            finally:
                # finallyは成功でもエラーでも必ず実行
                count+=1

        # 次のページボタンがあればクリックなければ終了
        next_page = driver.find_elements_by_class_name("iconFont--arrowLeft")
        if len(next_page) >= 1:
            next_page_link = next_page[0].get_attribute("href")
            driver.get(next_page_link)
        else:
            log1("最終ページです。終了します。")
            break

    # CSV出力
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    df = pd.DataFrame({"銘柄名":exp_name_list,
                       "現在値":exp_value_list,
                       "出来高":exp_volume_list,
                       "前日比":exp_comparison_list})
    df.to_csv(EXP_CSV_PATH.format(search_keyword=search_keyword,datetime=
                                  now), encoding="utf-8-sig")
    log1(f"処理完了 成功件数: {success} 件 / 失敗件数: {fail} 件")
    
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()