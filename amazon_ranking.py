import requests
from bs4 import BeautifulSoup


# Amazon ランキング　
# スクレイピング Tool
# 使い方
# pip install モジュール
#             requests
#			  BeautifulSoup4
#			  pandas 
#			  json
#
# python3 amazon_ranking.py
#
#

_target1 = 'dp/'
_target2 = '?_'

_url = "https://www.amazon.co.jp/"
_category = 'digital-text'
_browse_node_id = '2293143051'


info = []


def ama(load_url):
	# Webページを取得して解析する
	# 目的URL https://www.amazon.co.jp/gp/bestsellers/digital-text/2293143051/?pg=2
	html = requests.get(load_url)
	# ステータスコードでの
	try:
		html.raise_for_status()
	except Exception as exc:
		print('問題あり:{}'.format(exc))

	soup = BeautifulSoup(html.content, "html.parser")
	return soup



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
	idx = MAIN_PAGE_URL.find(_target1)  # 半角空白文字のインデックスを検索
	# 検索文字列の先頭文字の場所が idxに格納される
	retext = MAIN_PAGE_URL[idx+3:]
	idx2 = retext.find(_target2)
	ASIN = retext[:idx2]
	MAIN = _url + _target1 + ASIN

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


def main():
	load_url = _url + 'gp/bestsellers/' +  _category + '/' + _browse_node_id + '/' + '?pg=' + "1"
	print("++++++++++++++++++++++++++++++++++++++++++++++++")
	print(" ")
	print(load_url)
	print(" ")
	print("++++++++++++++++++++++++++++++++++++++++++++++++")
	soup = ama(load_url)
	# すべてのliタグを検索して、その文字列を表示する
	for ele in soup.find_all("li", class_="zg-item-immersion"):
		get_ViewInfo(ele)
  

if __name__ == '__main__':
    main()















