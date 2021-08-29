import requests
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options #headlessオプションに使用


# Amazon ランキング　
# スクレイピング Tool
# 使い方
# pip install モジュール
#             requests        ->> https://pypi.org/project/requests/
#			  BeautifulSoup4
#			  pandas 
#			  json
#			  selenium       ->> https://kakashi-blog.com/amazon%E3%81%AF%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0%E3%81%8C%E7%A6%81%E6%AD%A2%E3%80%82selenium%E3%81%A7%E3%83%87%E3%83%BC%E3%82%BF%E5%8F%8E%E9%9B%86%E3%82%92%E3%81%97/
#
#
# python3 amazon_ranking.py
#
#

_TARGET_WORD_1 = 'dp/'
_TARGET_WORD_2 = '?_'

_DRIVER = "/usr/local/bin/chromedriver" # 各環境のブラウザドラーバーのパスを設定
_BASE_URL = "https://www.amazon.co.jp/"
_CATEGORY = 'digital-text'
_BROWSE_NODE_ID = '2293143051'
_DEFAULT_BEAUTIFULSOUP_PARSER = "html.parser"
_TODAY = datetime.datetime.now().strftime('%Y.%m.%d-%H-%M')

_INFO_SUM = '10'
_DEBUG_FLAG = '0' #ON='1' OFF='0'
_DEBUG_VIEW = '1' #ON='1' OFF='0'
_DEBUG_CNT = 5
_DEBUG_FILE = '2021.07.31-22-07.json' #表示したいファイルを設定する
_DEBUG_FILE_VIEW_FLAG = '0' #ON='1'(_DEBUG_FILEを読み込み表示する) | OFF='0' 
_DICT_CNT = 0 #JSONファイル作成時の要素のカウントで使用

_dict_info = {}
_list_info = []

class get_sous:
    
    def __init__(self,url,browser):
        self.url=url
        self.browser=browser
        
    def getbrowser(self):
        sous=self.browser.page_source
        self.browser.close()
        return sous
        
    def openurl(self):
        self.browser.get(self.url)
        time.sleep(5)
        
    def search_(self,name):    
        search_name=self.browser.find_element_by_id('twotabsearchtextbox')
        search_name.clear()
        search_name.send_keys(name)
        btn=self.browser.find_element_by_class_name("nav-input")
        btn.click()
        time.sleep(5)

def open_selenium(load_url):
	# ブラウザーの設定
	option = Options()
	#ブラウザ非表示
	option.add_argument('--headless')
	# スクロールバー非表示
	#option.add_argument('--hide-scrollbars')
	# シークレットモード指定
	#option.add_argument('--incognito')
	# ユーザーエージェント指定
	#option.add_argument('--user-agent=hogehoge')
	# 言語指定
	#option.add_argument('--lang=ja')
	# SSLセキュリティを緩くする
	#option.add_argument('--ignore-certificate-errors')
	# 画像を読み込まない
	option.add_argument('--blink-settings=imagesEnabled=false')
	webd=webdriver.Chrome(_DRIVER,options=option)
	open1=get_sous(load_url,webd)
	# ブラウザーの起動
	open1.openurl()
	sous1=open1.getbrowser()
	soup=BeautifulSoup(sous1, 'html.parser')
	return soup


def get_summary(main_soup):
	# ここは実際に実行しデバック表示させて確認しないと抽出要素の基準が絞れないので注意
	# noscriptにはデコード?されていない文字列が入っていた。
	summary = main_soup.find("div", id="bookDescription_feature_div").find("noscript").text.strip()
	return summary

def get_release(main_soup):
	# 参考: https://qiita.com/Azunyan1111/items/b161b998790b1db2ff7a
	release = main_soup.select_one("#detailBullets_feature_div > ul > li:nth-child(3) > span > span:nth-child(2)").text
	return release

def get_publisher(main_soup):
	publisher = main_soup.select_one("ol.a-carousel > li:nth-child(2) > div > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span").text
	# たまに順番がずれている場合があるため"日本語"が来た場合後ろの値を再取得する
	if publisher == "日本語":
		publisher = main_soup.select_one("ol.a-carousel > li:nth-child(3) > div > div.a-section.a-spacing-none.a-text-center.rpi-attribute-value > span").text

	return publisher

# 型と中身を表示させる関数
def print_data(data):
    print(type(data))
    print(data)
    print(json.dumps(data,indent=int(_INFO_SUM), ensure_ascii=False ))

def ama(load_url):
	# ステータスコードでのリトライ
	# 参考: https://qiita.com/azumagoro/items/3402facf0bcfecea0f06
	session = requests.Session()
	retries = Retry(total=5,  # リトライ回数
                backoff_factor=1,  # sleep時間
                status_forcelist=[500, 502, 503, 504])  # timeout以外でリトライするステータスコード

	session.mount("https://", HTTPAdapter(max_retries=retries))
	
	# Webページを取得して解析する
	# 目的URL https://www.amazon.co.jp/gp/bestsellers/digital-text/2293143051/?pg=2
	# ステータスコードでの
	try:
		html = session.get(url=load_url,
	                       stream=True,
	                       timeout=(10.0, 30.0)) # connect timeoutを10秒, read timeoutを30秒に設定

	except requests.exceptions.ConnectTimeout:
		print('問題あり:タイムアウトしました')
		sys.exit()

	else:
		print(html.status_code)

	soup = BeautifulSoup(html.content, _DEFAULT_BEAUTIFULSOUP_PARSER)
	return soup


def get_info(ele):
	RANK = ele.find("span", class_="zg-badge-text").text
	TITLE = ele.find("div", class_="p13n-sc-truncate").text.strip()
	AUTHOR = ele.find("div", class_="a-row a-size-small").text
	PRICE = ele.find("span", class_="p13n-sc-price").text
	PICTURE_tag = ele.find("div", class_="a-section a-spacing-small")
	PICTURE_URL = PICTURE_tag.find("img").get("src")
	MAIN_PAGE_tag = ele.find("span", class_="aok-inline-block zg-item")
	MAIN_PAGE_URL = MAIN_PAGE_tag.find("a", class_="a-link-normal").get("href")

	PRICE = PRICE[1:]
	# 作品ページURLから無駄な文字列の削除
	idx = MAIN_PAGE_URL.find(_TARGET_WORD_1)  # 半角空白文字のインデックスを検索
	# 検索文字列の先頭文字の場所が idxに格納される
	#retext = MAIN_PAGE_URL[idx+3:idx+13] #dp/の3文字分をずらしてURLから10文字分スライス
	retext = MAIN_PAGE_URL[idx+3:] #dp/の3文字分をずらし
	idx2 = retext.find(_TARGET_WORD_2)
	ASIN = retext[:idx2]
	MAIN = _BASE_URL + _TARGET_WORD_1 + ASIN
	main_soup = open_selenium(MAIN)
	SUMMARY = get_summary(main_soup)
	RELEASE = get_release(main_soup)
	PUBLISHER = get_publisher(main_soup)

	#info 10項目
	info = {
	"ranking": RANK,
	"title": TITLE,
	"author": AUTHOR,
	"price": PRICE,
	"img": PICTURE_URL,
	"asin": ASIN,
	"url": MAIN,
	"summary": SUMMARY,
	"release": RELEASE,
	"publisher": PUBLISHER
	}

	if _DEBUG_VIEW == '1':
		print("Ranking : "+ RANK)
		print("Title   : "+ TITLE)
		#Score系は 評価のない新刊に対してErrとなるため 一旦保留
		#print("Score   : "+ element.find("i", class_="a-icon a-icon-star a-star-5 aok-align-top").text)
		#print("ScoreSUM: "+ element.find("a", class_="a-size-small a-link-normal").text)
		print("Author  : "+ AUTHOR)
		print("Price   : "+ PRICE)
		print("Picture : "+ PICTURE_URL)
		print("Asin    : "+ ASIN)
		print("MainPage: "+ MAIN)
		print("SUMMARY : "+ SUMMARY)
		print("Release : "+ RELEASE)
		print("PUB     : "+ PUBLISHER)
		print("= = = = = = = = = = =  = = = = = = = =  = = = = = = =  = = = = =  = = = =  =")

	return info

	
def write(_dict,_list):
	time.sleep(2)
	# utf-8で書き込み
	with open('Amazon' + str(_TODAY) + '_id付' + '.json', 'w', encoding='utf-8_sig') as fp:
		# 辞書(info)をインデントをつけてアスキー文字列ではない形で保存
	    json.dump(_dict, fp, indent=int(_INFO_SUM), ensure_ascii=False )
	# 書き込みオブジェクトを閉じる
	fp.close()
	# utf-8で書き込み
	with open('Amazon' + str(_TODAY) + '.json', 'w', encoding='utf-8_sig') as fp:
		# 辞書(info)をインデントをつけてアスキー文字列ではない形で保存
	    json.dump(_list, fp, indent=int(_INFO_SUM), ensure_ascii=False )
	# 書き込みオブジェクトを閉じる
	fp.close()

	#pandasを使用してCSV形式で出力
	df = pd.DataFrame(_list)
	df.to_csv('Amazon' + str(_TODAY) + '.csv',encoding='utf-8_sig')  


	
def json_data_view():
	#取得したJsonデータを表示
	if _DEBUG_FILE_VIEW_FLAG == '0':
		with open('Amazon' + str(_TODAY) + '.json', 'r', encoding='utf-8_sig') as fp:
			data = json.load(fp)
	else :
		with open(_DEBUG_FILE, 'r', encoding='utf-8_sig') as fp:
			data = json.load(fp)

	# 書き込みオブジェクトを閉じる
	fp.close()
	print_data(data)


def get_data(load_url):
	global _DICT_CNT
	print("++++++++++++++++++++++++++++++++++++++++++++++++")
	print(" ")
	print(load_url)
	print(" ")
	print("++++++++++++++++++++++++++++++++++++++++++++++++")
	soup = ama(load_url)
	# すべてのliタグを検索して、その文字列を表示する
	for ele in soup.find_all("li", class_="zg-item-immersion"):
		
		_num = 'id_'+ str(_DICT_CNT) #要素の管理番号
		_dict = get_info(ele)		 #取得データを辞書型で代入
		_dict_info[_num] = _dict 	 #要素の管理番号をキーにしValueに辞書型の取得データを格納
		_list_info.append(_dict) 	 #CSV出力用にキーなしの辞書型のデータを追加
		_DICT_CNT+=1
									 # Debug用 _DEBUG_CNTで取得を中断
		if _DEBUG_FLAG == '1':
			if _DEBUG_CNT < _DICT_CNT+1:
				break


def main():

	if _DEBUG_FLAG == '0':
		for n in range(1,3):
			load_url = _BASE_URL + 'gp/bestsellers/' +  _CATEGORY + '/' + _BROWSE_NODE_ID + '/' + '?pg=' + str(n)
			get_data(load_url)
	else :
		print("DEBUG_FLAG :"+ _DEBUG_FLAG)
		print("DEBUG_VIEW :"+ _DEBUG_VIEW)
		print("DEBUG_CNT  :"+ str(_DEBUG_CNT))
		load_url = _BASE_URL + 'gp/bestsellers/' +  _CATEGORY + '/' + _BROWSE_NODE_ID + '/' + '?pg=' + '1'
		get_data(load_url)

	#ファイルへの出力
	write(_dict_info,_list_info)

if __name__ == '__main__':

	if _DEBUG_FILE_VIEW_FLAG == '0':
		main()
		json_data_view()
	else :
		json_data_view()















