# -*- coding: utf-8 -*-
import time
from datetime import datetime
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.posts import GetPostStatusList
import configparser
"""
扱う変数;title,content,slug
pip install python-wordpress-xmlrpc　
"""
def post_article(title,content,slug):
    #idとpasswordはwordpressの管理画面に入るためのもの
    config = configparser.ConfigParser()
    config.read('meigaku/config.py')
    jsonf = config['Googlesheet']['jsonf']
    spread_sheet_key = config['Googlesheet']['spread_sheet_key']
    id = config['WORDPRESS']['id']
    password = config['WORDPRESS']['password']

    url="https://gakuseikoujyou.com/xmlrpc.php"
    #第3者が閲覧するURLの後ろに/xmlrpc.phpをつける。
    #ワードプレスの管理画面の後ろにつけるとエラーになった

    which="draft"
    #which="draft"
    #下書きに投稿するか本番で投稿するか選択
    wp = Client(url, id,password)
    post = WordPressPost()
    post.post_status = which
    post.title = title
    post.content = content
    post.slug=slug
    post.terms_names = {
    "post_tag": [],
    "category": [],
    }
# if __name__=='__main__':
#     post_article('a','b','c')

"""
########動作テスト#########
title="野球"
content="今年は野球を始めます"
slug="start_baseball"
post_article(title,content,slug)
print("投稿成功")
"""



