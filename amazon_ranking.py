import requests
#from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup


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
_DEFAULT_USER_AGENT = 'Mozilla/5.0 (Linux; Android 7.0; \
SM-A520F Build/NRD90M; wv) AppleWebKit/537.36 \
(KHTML, like Gecko) Version/4.0 \
Chrome/65.0.3325.109 Mobile Safari/537.36'
_CHROME_DESKTOP_USER_AGENT = 'Mozilla/5.0 (Macintosh; \
Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/67.0.3396.79 Safari/537.36'

_USER_AGENT_LIST = [
    _DEFAULT_USER_AGENT,
    _CHROME_DESKTOP_USER_AGENT,
]


info = []


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
		soup = BeautifulSoup(html.content, _DEFAULT_BEAUTIFULSOUP_PARSER)
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
	idx = MAIN_PAGE_URL.find(_TARGET_WORD_1)  # 半角空白文字のインデックスを検索
	# 検索文字列の先頭文字の場所が idxに格納される
	retext = MAIN_PAGE_URL[idx+3:]
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


def main():
	load_url = _BASE_URL + 'gp/bestsellers/' +  _CATEGORY + '/' + _BROWSE_NODE_ID + '/' + '?pg=' + "1"
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















