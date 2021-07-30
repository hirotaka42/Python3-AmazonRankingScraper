import requests
#from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import json
from selenium import webdriver


# Amazon ランキング　
# スクレイピング Tool
# 使い方
# pip install モジュール
#             requests        ->> https://pypi.org/project/requests/
#			  BeautifulSoup4
#			  pandas 
#			  json
#
# python3 amazon_ranking.py
#
#

_TARGET_WORD_1 = 'dp/'
_TARGET_WORD_2 = '?_'

_DRIVER = "/usr/local/bin/chromedriver" 
_BASE_URL = "https://www.amazon.co.jp/"
_CATEGORY = 'digital-text'
_BROWSE_NODE_ID = '2293143051'
_DEFAULT_BEAUTIFULSOUP_PARSER = "html.parser"
_TODAY = datetime.datetime.now().strftime('%Y.%m.%d-%H-%M')

_INFO_SUM = '8'
info = []

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

def get_summary(load_url):
	webd=webdriver.Chrome(_DRIVER)
	open1=get_sous(load_url,webd)
	open1.openurl()
	sous1=open1.getbrowser()
	main_soup=BeautifulSoup(sous1, 'html.parser')
	# ここは実際に実行しデバック表示させて確認しないと抽出要素の基準が絞れないので注意
	# noscriptにはデコードされていない文字列が入っていた。
	summary = main_soup.find("div", id="bookDescription_feature_div").find("noscript").text.strip()
	return summary

# 型と中身を表示させる関数
def print_data(data):
    print(type(data))
    print(data)

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

	# 作品ページから無駄な文字列の削除
	idx = MAIN_PAGE_URL.find(_TARGET_WORD_1)  # 半角空白文字のインデックスを検索
	# 検索文字列の先頭文字の場所が idxに格納される
	#retext = MAIN_PAGE_URL[idx+3:idx+13] #dp/の3文字分をずらしてURLから10文字分スライス
	retext = MAIN_PAGE_URL[idx+3:] #dp/の3文字分をずらし
	idx2 = retext.find(_TARGET_WORD_2)
	ASIN = retext[:idx2]
	MAIN = _BASE_URL + _TARGET_WORD_1 + ASIN
	summary = get_summary(MAIN)

	#info 8項目
	info = {
	"ranking": RANK,
	"title": TITLE,
	"author": AUTHOR,
	"price": PRICE,
	"img": PICTURE_URL,
	"asin": ASIN,
	"url": MAIN,
	"summary": summary
	}

	return info


def get_ViewInfo(ele):
	RANK = ele.find("span", class_="zg-badge-text").text
	TITLE = ele.find("div", class_="p13n-sc-truncate").text.strip()
	AUTHOR = ele.find("div", class_="a-row a-size-small").text
	PRICE = ele.find("span", class_="p13n-sc-price").text
	PICTURE_tag = ele.find("div", class_="a-section a-spacing-small")
	PICTURE_URL = PICTURE_tag.find("img").get("src")
	MAIN_PAGE_tag = ele.find("span", class_="aok-inline-block zg-item")
	MAIN_PAGE_URL = MAIN_PAGE_tag.find("a", class_="a-link-normal").get("href")

	# 作品ページから無駄な文字列の削除
	idx = MAIN_PAGE_URL.find(_TARGET_WORD_1)  # 半角空白文字のインデックスを検索
	# 検索文字列の先頭文字の場所が idxに格納される
	#retext = MAIN_PAGE_URL[idx+3:idx+13] #dp/の3文字分をずらしてURLから10文字分スライス
	retext = MAIN_PAGE_URL[idx+3:] #dp/の3文字分をずらし
	idx2 = retext.find(_TARGET_WORD_2)
	ASIN = retext[:idx2]
	MAIN = _BASE_URL + _TARGET_WORD_1 + ASIN
	summary = get_summary(MAIN)

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
	print("SUMMARY : "+ summary)
	print("= = = = = = = = = = =  = = = = = = = =  = = = = = = =  = = = = =  = = = =  =")

def write(info):
	time.sleep(2)
	# utf-8で書き込み
	with open('Amazon' + str(_TODAY) + '.json', 'w', encoding='utf-8_sig') as fp:
		# 辞書(info)をインデントをつけてアスキー文字列ではない形で保存
	    json.dump(info, fp, indent=8, ensure_ascii=False )
	# 書き込みオブジェクトを閉じる
	fp.close()

	#pandasを使用してCSV形式で出力
	df = pd.DataFrame(info)
	df.to_csv('Amazon' + str(_TODAY) + '.csv',encoding='utf-8_sig')  


	
def data_view():
	#取得したJsonデータを表示
	with open('Amazon' + str(_TODAY) + '.json', 'r', encoding='utf-8_sig') as fp:
		data = json.load(fp)

	# 書き込みオブジェクトを閉じる
	fp.close()
	print_data(data)


def main():
	for n in range(1,3):
		load_url = _BASE_URL + 'gp/bestsellers/' +  _CATEGORY + '/' + _BROWSE_NODE_ID + '/' + '?pg=' + str(n)
		print("++++++++++++++++++++++++++++++++++++++++++++++++")
		print(" ")
		print(load_url)
		print(" ")
		print("++++++++++++++++++++++++++++++++++++++++++++++++")
		soup = ama(load_url)
		# すべてのliタグを検索して、その文字列を表示する
		for ele in soup.find_all("li", class_="zg-item-immersion"):
			#get_ViewInfo(ele)
			info.append(get_info(ele))

		write(info)


def debug_main():
	load_url = _BASE_URL + 'gp/bestsellers/' +  _CATEGORY + '/' + _BROWSE_NODE_ID + '/' + '?pg=' + '1'
	print("++++++++++++++++++++++++++++++++++++++++++++++++")
	print(" ")
	print(load_url)
	print(" ")
	print("++++++++++++++++++++++++++++++++++++++++++++++++")
	soup = ama(load_url)
	# すべてのliタグを検索して、その文字列を表示する
	for ele in soup.find_all("li", class_="zg-item-immersion"):
		#get_ViewInfo(ele)
		info.append(get_info(ele))

	write(info)
	


if __name__ == '__main__':
    main()
    #debug_main()
    data_view()















