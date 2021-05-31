from selenium import webdriver
import time
import configparser

config=configparser.ConfigParser()
config.read('meigaku/config.py')
jsonf=config['Googlesheet']['jsonf']
spread_sheet_key=config['Googlesheet']['spread_sheet_key']
id=config['WORDPRESS']['id']
password=config['WORDPRESS']['password']

#投稿編集画面への遷移
def move_post_list():
    server_url=config['server']['server_url']
    sever_id=config['server']['server_id']
    server_pass=config['server']['server_pass']

    wordpress_url=config['wordpress_login']['wordpress_url']
    wordpress_id=config['wordpress_login']['wordpress_id']
    wordpress_pass=config['wordpress_login']['wordpress_pass']

    # google chromeの起動
    browser = webdriver.Chrome()
    browser.implicitly_wait(2)

    browser.get(server_url)
    time.sleep(2)
    print("サーバー管理へログイン")
    #サーバー　elementを取得
    server_element_username=browser.find_element_by_name("username")
    server_element_password=browser.find_element_by_id("server_password")
    server_element_login=browser.find_element_by_id("submit-btn")

    server_element_username.clear()
    server_element_password.clear()

    server_element_username.send_keys(sever_id)
    server_element_password.send_keys(server_pass)
    server_element_login.click()
    browser.implicitly_wait(2)
    print("サーバー管理画面ログイン完了")
    # wordpress編集へ
    print(browser.find_element_by_link_text("http://gakuseikoujyou.com/wp-admin/"))
    browser.find_element_by_link_text("http://gakuseikoujyou.com/wp-admin/").click()
    time.sleep(2)
    print("ログイン画面")

    browser.get(wordpress_url)
    name = browser.find_element_by_xpath("//input[@id='user_login']")
    password = browser.find_element_by_xpath("//input[@id='user_pass']")
    name.send_keys(wordpress_id)
    password.send_keys(wordpress_pass)

    login_btn = browser.find_element_by_xpath(".//input[@id='wp-submit']")
    login_btn.click()
    browser.implicitly_wait(2)
    print("ログイン成功")
    return browser