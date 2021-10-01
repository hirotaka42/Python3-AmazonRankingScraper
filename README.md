# 概要
Amazon Kindle人気ランキング 取得
スクレイピング Tool

## 使用モジュール
requests    
BeautifulSoup4    
pandas    
json    
selenium    
webdriver-manager    

## モジュール詳細

```vim:
https://pypi.org/project/requests/
https://pypi.org/project/beautifulsoup4/
https://pypi.org/project/pandas/
https://pypi.org/project/selenium/
https://pypi.org/project/webdriver-manager/

https://kakashi-blog.com/amazon%E3%81%AF%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0%E3%81%8C%E7%A6%81%E6%AD%A2%E3%80%82selenium%E3%81%A7%E3%83%87%E3%83%BC%E3%82%BF%E5%8F%8E%E9%9B%86%E3%82%92%E3%81%97/    

https://yuki.world/python-selenium-chromedriver-auto-update/
```

## import 

```vim:
import requests
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import time     #python3に組み込まれているためimportだけで使用できる
import datetime #python3に組み込まれているためimportだけで使用できる
import json     #python3に組み込まれているためimportだけで使用できる
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options #headlessオプションに使用
from webdriver_manager.chrome import ChromeDriverManager 
```


## 実行方法
python3 amazon_ranking.py    


### package install

`pip3 install <package-name>==<version>`

```bash:
pip3 install requests
pip3 install beautifulsoup4
pip3 install pandas 
pip3 install json
pip3 install selenium
pip3 install webdriver-manager
```

### update

```bash:
pip install -U <package-name>
```

### updateがあるもの

```bash:
pip3 list -o
pip3 list -o | tail -n +3 | awk '{ print $1 }' | xargs pip3 install -U
alias pip-upgrade-all="pip3 list -o | tail -n +3 | awk '{ print \$1 }' | xargs pip3 install -U"

"ERROR: Could not install packages due to an OSError"
このようなErrが出ることがある。
権限が無いことが原因のためオプションとして"--user"を付けてあげることで解決することが出来る。
pip3 install <package-name> --user
pip3 list -o | tail -n +3 | awk '{ print $1 }' | xargs pip3 install -U --user

```

### 依存関係のcheck

`pip3 check`

### install packege の表示

`pip3 list`

### update不要のものを表示

`pip3 list -u`

### パッケージをパッケージ名==バージョンで表示

```bash:
pip3 freeze
pip3 freeze > requirements.txt
```

