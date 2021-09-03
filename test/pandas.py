#seleniumはブラウザを自動で操作してくれる

from selenium import webdriver
import time
import pandas as pd
import os
import datetime

USER = "test_user"
PASS = "test_pw"

#GoogleChromeを起動
browser = webdriver.Chrome(executable_path = "C:\\Users\\81904\\Desktop\\Mypandas\\chromedriver.exe")
browser.implicitly_wait(3)

#ログインするサイトへアクセス
url_login = "https://kino-code.com/membership-login/"
browser.get(url_login)
time.sleep(3)
print("ログインページにアクセスしました")

elem = browser.find_element_by_id("swpm_user_name")
elem.clear()
elem.send_keys(USER)
elem = browser.find_element_by_id("swpm_password")
elem.clear()
elem.send_keys(PASS)
print("フォームを送信")

#入力したデータをクリック
browser_from = browser.find_element_by_class_name("swpm-login")
time.sleep(3)
browser_from.click()
print("情報を入力してログインボタンを押しました")

#ウェブサイトへアクセス
url="http://kino-code.com/member-only/"
time.sleep(1)
browser.get(url)
print(url,":アクセス完了")

#ダウンロードボタンをクリック
frm = browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/main/article/div/p[2]/button")#ダウンロードの検証右クリックcoppyのXpassをcoppy
time.sleep(1)
frm.click()
print("ダウンロードボタンをクリック")
quit()
