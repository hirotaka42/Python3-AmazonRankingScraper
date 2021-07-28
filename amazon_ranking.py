import requests
#from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import json


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

_BASE_URL = "https://www.amazon.co.jp/"
_CATEGORY = 'digital-text'
_BROWSE_NODE_ID = '2293143051'
_DEFAULT_BEAUTIFULSOUP_PARSER = "html.parser"
_TODAY = datetime.datetime.now().strftime('%Y.%m.%d-%H-%M')

info = []

# 型と中身を表示させる関数
def print_data(data):
    print(type(data))
    print(data)

def ama(load_url):
	# ステータスコードでのリトライ
	# 参考: https://qiita.com/azumagoro/items/3402facf0bcfecea0f06
	time.sleep(2)
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

	print(html.text[:500])
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

	info = {
	"ranking": RANK,
	"title": TITLE,
	"author": AUTHOR,
	"price": PRICE,
	"img": PICTURE_URL,
	"asin": ASIN,
	"url": MAIN
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
	print("= = = = = = = = = = =  = = = = = = = =  = = = = = = =  = = = = =  = = = =  =")

def write(info):
	time.sleep(2)
	# utf-8で書き込み
	with open('Amazon' + str(_TODAY) + '.json', 'w', encoding='utf-8_sig') as fp:
		# 辞書(info)をインデントをつけてアスキー文字列ではない形で保存
	    json.dump(info, fp, indent=7, ensure_ascii=False )
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
			get_ViewInfo(ele)
			info.append(get_info(ele))

		write(info)
	


if __name__ == '__main__':
    main()
    data_view()















