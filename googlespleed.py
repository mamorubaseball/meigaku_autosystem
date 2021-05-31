import gspread
from oauth2client.service_account import ServiceAccountCredentials
# import ChangeToRoma
from wordpress_xmlrpc.methods.posts import DeletePost
from datetime import datetime
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
#import scraping
import time
import csv
import configparser

"""
#######################googlespreadsheetの書き方############
val = worksheet.cell(1, 2).value
###########################取得する変数名#####################
   記事を投稿して成功した場合はTrue、失敗した場合はFalseを返します。
   :param status: 記事の状態（公開:publish, 下書き:draft）
   :param slug: 記事識別子。URLの一部になる（ex. slug=aaa-bbb/ccc -> https://wordpress-example.com/aaa-bbb/ccc）
   :param title: 記事のタイトル
   :param content: 記事の本文
   :param category_ids: 記事に付与するカテゴリIDのリスト
   :param tag_ids: 記事に付与するタグIDのリスト
   :param media_id: 見出し画像のID
   :return: レスポンス
######install###################################
pyhtonはjsonが標準モジュールなので、gspreadとoauth2clientをinstall
pip install gspread
pip install oauth2client

####進捗情報###########2020/12/20###############
get_informationで情報を取得は可能？
get_informationで得た情報を変数に入れて代入ができないの？
googlespleedの指定した項目は投稿可能
######課題##########2020/12/20
num(投稿記事の行番号)⇨何番目のサークルを掲載するか
####課題############2020/12/28
重複する投稿は避けたい
カテゴリー、画像、説明の指定
"""

config=configparser.ConfigParser()
config.read('meigaku/config.py')
jsonf=config['Googlesheet']['jsonf']
spread_sheet_key=config['Googlesheet']['spread_sheet_key']
id=config['WORDPRESS']['id']
password=config['WORDPRESS']['password']
# (1) Google Spread Sheetsにアクセス
def connect_gspread(jsonf,key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key(key).sheet1
    all=worksheet.get_all_values()
    column_number=len(all)
    return worksheet,column_number
#(2)　googleSpreadsheetびidを追加

def input_data_to_googlespreadsheet():
    #wordpress_title_id_list=scraping.get_wordpress_titile()
    googlespread=connect_gspread(jsonf,spread_sheet_key)[0]
    number=connect_gspread(jsonf,spread_sheet_key)[1]
    with open("meigaku.csv", "r") as f:
        reader=csv.reader(f)
        print(number)
        for i in range(number//10):
            for read in reader:
                if googlespread.acell("C" + str(i+2)).value == read[0]:
                    googlespread.update("AE" + str(i+2), read[1])
                    time.sleep(3)
    f.close()
def get_information(gs,num):
    title=gs.cell(num ,3).value
    content=gs.cell(num ,28).value
    media_id=gs.cell(num ,28).value
    # slug=ChangeToRoma.ChangeToRoma(title)
    return title,content

#####wordpress#############
#削除機能
def delete_wordpress():
    DeletePost(id)
def post_meigaku(index):
    title,content,slug = get_information(index)
    #titileを比較
    post_article(title, content, slug)

def new_post_meigaku():
    gs,now_index = connect_gspread(jsonf, spread_sheet_key)
    for index in range(105,now_index)+1:
        post_meigaku(index)
def post_article(title,content,slug):
    #idとpasswordはwordpressの管理画面に入るためのもの

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
    post.date=datetime.now()
    wp.call(NewPost(post))

if __name__=="__main__":
    gs,num=connect_gspread(jsonf, spread_sheet_key)
    slug='id'
    for i in range(104,num+1):
        title,content=get_information(gs,i)
        post_article(title,content,slug)



