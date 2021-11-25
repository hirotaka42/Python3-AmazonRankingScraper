# Python3-AmazonRankingScraper

## Overview

Amazon Kindleランキングの情報を取得します。

出力形式

- CSV
- JSON

## Prerequisite

python >= 3.8   
chromeブラウザ

## Installation

### linux

```
$ python -m venv venv
$ . ./venv/bin/activate
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt
$ python amazon_ranking.py    
```

### Mac

```
# git clone
git clone https://github.com/hirotaka42/Python3-AmazonRankingScraper.git
cd Python3-AmazonRankingScraper

# venv(仮想環境) を作成
python3 -m venv venv

# venv を有効化
. ./venv/bin/activate
# もしくわ
source ./venv/bin/activate

# venv内の pipをアップグレード
python3 -m pip install --upgrade pip
# モジュール の install 
pip install -r requirements.txt

# venv内で実行
python3 amazon_ranking.py
# 100件の商品ページへブラウザ経由でアクセスする。
# その為、おおよそ15分-30分程時間がかかる。

# 終了したら仮想環境を終了
deactivate

# 2回目以降 (venv有効化し、実行)
source ./venv/bin/activate
python3 amazon_ranking.py
```

## mac 一括実行(コピペ用)
```
# git clone
git clone https://github.com/hirotaka42/Python3-AmazonRankingScraper.git
cd Python3-AmazonRankingScraper

# venv(仮想環境) を作成
python3 -m venv venv && \
source ./venv/bin/activate && \
python3 -m pip install --upgrade pip && \
pip install -r requirements.txt && \
python3 amazon_ranking.py

# 100件の商品ページへブラウザ経由でアクセスする。
# その為、おおよそ15分-30分程時間がかかる。

# 終了したら仮想環境を終了
deactivate

# 2回目以降 (venv有効化し、実行)
source ./venv/bin/activate
python3 amazon_ranking.py
```

## How to use

```
python3 amazon_ranking.py
# 100件の商品ページへブラウザ経由でアクセスする。
# その為、おおよそ15分-30分程時間がかかる。
```

![スクリーンショット 2021-11-26 2 13 19](https://user-images.githubusercontent.com/79750434/143481405-aff0ab15-9550-42e9-9af3-6db6c9ca73f3.png)
![スクリーンショット 2021-11-26 2 13 38](https://user-images.githubusercontent.com/79750434/143481441-84b3dac8-a38a-4c3a-9504-ffdd680e62f9.png)
