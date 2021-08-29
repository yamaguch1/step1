#丸コピ
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

HEADER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"

def set_driver(is_headless: bool=False):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモードの設定
    if is_headless:
        options.add_argument('--headless')
        
    options.add_argument('--user-agent=' + HEADER_USER_AGENT)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与
    
    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(ChromeDriverManager().install(), options=options)

url = "https://www.sbisec.co.jp/ETGate/?_ControlID=WPLEThmR001Control&_PageID=DefaultPID&_DataStoreID=DSWPLEThmR001Control&_ActionID=DefaultAID&getFlg=on"

driver = set_driver()
driver.get(url)
driver.find_element_by_id("top_stock_sec").send_keys("アフリカ")
driver.find_element_by_css_selector("[title='株価検索']").click()
time.sleep(3)
name_elms = driver.find_elements_by_css_selector(".accTbl01 tr td:nth-child(1) p:first-child")
price_elms = driver.find_elements_by_css_selector(".accTbl01 tr td:nth-child(3) p")
df = pd.DataFrame()
for name_elm, price_elm in zip(name_elms, price_elms):
    df = df.append({
        "銘柄名": name_elm.text,
        "現在値": price_elm.text.replace(",", "")
    }, ignore_index=True)
    
df.to_csv("export.csv", encoding="utf-8_sig")