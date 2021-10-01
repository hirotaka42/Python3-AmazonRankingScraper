# 概要
Amazon Kindle人気ランキング 取得
スクレイピング Tool

## 使用モジュールのインストール

pip3 install モジュール
requests      -->> pip3 install requests
              |->> https://pypi.org/project/requests/
BeautifulSoup4-->> pip3 install beautifulsoup4
              |->> https://pypi.org/project/beautifulsoup4/
pandas 

json
selenium      -->>
              |->> https://kakashi-blog.com/amazon%E3%81%AF%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0%E3%81%8C%E7%A6%81%E6%AD%A2%E3%80%82selenium%E3%81%A7%E3%83%87%E3%83%BC%E3%82%BF%E5%8F%8E%E9%9B%86%E3%82%92%E3%81%97/
chrom Driver  -->> pip3 install webdriver-manager
              |->> https://yuki.world/python-selenium-chromedriver-auto-update/


## 実行方法
python3 amazon_ranking.py


pip3 install requests
pip3 install beautifulsoup4
pip3 install pandas
pip3 install webdriver-manager

#update
pip install -U <package-name>

#updateがあるもの
pip3 list -o
pip3 list -o | tail -n +3 | awk '{ print $1 }' | xargs pip3 install -U
alias pip-upgrade-all="pip3 list -o | tail -n +3 | awk '{ print \$1 }' | xargs pip3 install -U"

"ERROR: Could not install packages due to an OSError"
このようなErrが出ることがある。
権限が無いことが原因のためオプションとして"--user"を付けてあげることで解決することが出来る。
pip3 install <package-name> --user
pip3 list -o | tail -n +3 | awk '{ print $1 }' | xargs pip3 install -U --user





pip3 install <package-name>==<version>

pip3 check
pip3 list

#update不要のもの
pip3 list -u


#パッケージをパッケージ名==バージョンで表示
pip3 freeze
pip3 freeze > requirements.txt

