from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
import chromedriver_binary

import time
# from meigaku.wordpress_login import move_post_list
import os
import csv
import configparser
"""
versionエラー；
https://pypi.org/project/chromedriver-binary/#history
にアクセスして、現バージョンの確認と更新
１　今のgooglechromeのバージョンを確認
2　１で確認したバージョンに合わせてインストールする

"""

config=configparser.ConfigParser()
config.read('meigaku/config.py')
server_url=config['server']['server_url']
sever_id=config['server']['server_id']
server_pass=config['server']['server_pass']

wordpress_url=config['wordpress_login']['wordpress_url']
wordpress_id=config['wordpress_login']['wordpress_id']
wordpress_pass=config['wordpress_login']['wordpress_pass']


def move_post_list():
    # google chromeの起動
    browser = webdriver.Chrome()
    browser.implicitly_wait(2)
    browser.get(server_url)
    time.sleep(3)
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
    browser.implicitly_wait(3)
    print("サーバー管理画面ログイン完了")
    # wordpress編集へ
    # browser.get('https://secure.xserver.ne.jp/xserver/sv8578/?action_user_autoinstallwp_list=true&back=user_autoinstallwp_list&did=gakuseikoujyou.com')
    browser.find_element_by_link_text('WordPress簡単インストール').click()
    linktext=browser.find_elements_by_link_text('選択する')
    linktext[0].click()
    browser.find_element_by_link_text("http://gakuseikoujyou.com/wp-admin/").click()
    time.sleep(3)
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

def get_id_titile_url():
    browser=move_post_list()
    #  投稿一覧画面
    browser.find_element_by_link_text("投稿一覧").click()
    title=browser.find_element_by_id("the-list").find_elements_by_class_name("row-title").text
    id=browser.find_element_by_id("the-list").find_elements_by_class_name("post-id column-post-id").text
    # parmalinkの取得のため、編集画面
    browser.find_element_by_id("the-list").find_elements_by_class_name("row-title").click()
    url=browser.find_element_by_id("sample-permalink").find_element_by_tag_name('a').get_attribute('href')
    browser.implicitly_wait(3)
    return title,url,id

def draft_to_open(wordpress_id,wordpress_pass):
    browser=move_post_list()
    browser.find_element_by_link_text("投稿一覧").click()
    tr_list = browser.find_element_by_id("the-list").find_elements_by_tag_name("tr")
    for tr in tr_list:
        tr.find_element_by_class_name('button-link editinline').click()
        tr.find_element_by_name('_status').elect_by_value('publish')
        tr.find_element_by_class_name('button button-primary save alignright').click()
    print('投稿完了')
def get_wordpress_titile_id_url():
    # google chromeの起動
    browser = webdriver.Chrome()
    browser.implicitly_wait(2)
    browser.get(server_url)
    time.sleep(3)
    print("サーバー管理へログイン")
    # サーバー　elementを取得
    server_element_username = browser.find_element_by_name("username")
    server_element_password = browser.find_element_by_id("server_password")
    server_element_login = browser.find_element_by_id("submit-btn")

    server_element_username.clear()
    server_element_password.clear()

    server_element_username.send_keys(sever_id)
    server_element_password.send_keys(server_pass)
    server_element_login.click()
    browser.implicitly_wait(3)
    print("サーバー管理画面ログイン完了")
    # wordpress編集へ
    # browser.get('https://secure.xserver.ne.jp/xserver/sv8578/?action_user_autoinstallwp_list=true&back=user_autoinstallwp_list&did=gakuseikoujyou.com')
    browser.find_element_by_link_text('WordPress簡単インストール').click()
    linktext = browser.find_elements_by_link_text('選択する')
    linktext[0].click()
    browser.find_element_by_link_text("http://gakuseikoujyou.com/wp-admin/").click()
    time.sleep(3)
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
    # 明学ナビホームページから情報を取得
    browser.find_element_by_link_text('明学ナビ').click()
    with open("meigaku_id.csv", "w") as f:
        writer=csv.writer(f)
        writer.writerow(["title","url","ID"])

        a_tags=browser.find_elements_by_tag_name('a')
        url_list=[a.get_attribute('href') for a in a_tags]
        for url in url_list:
            browser.get(url)
        # li_lists=browser.find_element_by_tag_name('footer').find_element_by_tag_name('ul').find_elements_by_tag_name('li')
        url_list=['sports/','%e3%82%b9%e3%83%9d%e3%83%bc%e3%83%84%ef%bc%88%e7%90%83%e6%8a%80%e4%bb%a5%e5%a4%96%ef%bc%89/','%e5%9b%bd%e9%9a%9b%e4%ba%a4%e6%b5%81/','%e6%96%87%e5%8c%96%e7%b3%bb/','%e3%83%9c%e3%83%a9%e3%83%b3%e3%83%86%e3%82%a3%e3%82%a2/','%e3%82%a4%e3%83%99%e3%83%b3%e3%83%88%e7%b3%bb/','%e9%9f%b3%e6%a5%bd/']
        """
        親カテゴリー
        https://gakuseikoujyou.com/category/sports/
        https://gakuseikoujyou.com/category/%e3%82%b9%e3%83%9d%e3%83%bc%e3%83%84%ef%bc%88%e7%90%83%e6%8a%80%e4%bb%a5%e5%a4%96%ef%bc%89/
        https://gakuseikoujyou.com/category/%e5%9b%bd%e9%9a%9b%e4%ba%a4%e6%b5%81/
        https://gakuseikoujyou.com/category/%e6%96%87%e5%8c%96%e7%b3%bb/
        https://gakuseikoujyou.com/category/%e3%83%9c%e3%83%a9%e3%83%b3%e3%83%86%e3%82%a3%e3%82%a2/
        https://gakuseikoujyou.com/category/%e3%82%a4%e3%83%99%e3%83%b3%e3%83%88%e7%b3%bb/
        https://gakuseikoujyou.com/category/%e9%9f%b3%e6%a5%bd/
        """
        for url in url_list:
            browser.get('https://gakuseikoujyou.com/category/'+str(url))
            page_numbers=browser.find_element_by_class_name('pagination').find_elements_by_class_name('page-numbers')
            page_num=len(page_numbers)
            print(page_num)
            time.sleep(1)
            for i in range(page_num-2):
                articles=browser.find_element_by_id('list').find_elements_by_tag_name('a')
                for article in articles:
                    name=article.find_element_by_tag_name('h2').text
                    subscript=article.find_element_by_class_name('entry-card-snippet').text
                    url=article.get_attribute('href')

                    writer.writerow([name,url,subscript[:130]])
                    time.sleep(1)
                browser.find_element_by_class_name('pagination-next').find_element_by_tag_name('a').click()
            #明学ナビページに戻る必要がある
            browser.get('https://gakuseikoujyou.com/')

if __name__=='__main__':
    get_wordpress_titile_id_url()




























