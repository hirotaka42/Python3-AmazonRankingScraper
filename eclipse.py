import os
from pathlib import Path
import json

_DEBUG_PRINT = 1
_DEBUG_FILE = '' #出力したいjsonファイル
_INFO_SUM = 10 #インデントに設定をする要素数
_SELECT_FLAG = 99 # 0,1,2,3

print('0:output eclips Text  1: only "id_99"  2:json.dumps ')
val = input('Enter Select number :')

try:
    _SELECT_FLAG = int(val)

except ValueError:
    _SELECT_FLAG = 99


p = Path(".")
files = files = list(p.glob("./*_id*.json"))
file_updates = {file_path: os.stat(file_path).st_mtime for file_path in files}
newst_file_path = max(file_updates, key=file_updates.get)
_DEBUG_FILE = str(newst_file_path)

if _DEBUG_PRINT==1:
    print(_DEBUG_FILE)

with open(_DEBUG_FILE, 'r', encoding='utf-8_sig') as f:
    jsn = json.load(f)



if _SELECT_FLAG == 0:
    for jsn_val in jsn.values():
        print("map = new HashMap<>();")
        print('map.put("ranking"' + "," + '"' + jsn_val["ranking"] + '");')
        print('map.put("title"' + "," + '"' + jsn_val["title"] + '");')
        print('map.put("author"' + "," + '"' + jsn_val["author"] + '");')
        print('map.put("price"' + "," + '"' + jsn_val["price"] + '");')
        print('map.put("img"' + "," + '"' + jsn_val["img"] + '");')
        print('map.put("asin"' + "," + '"' + jsn_val["asin"] + '");')
        print('map.put("url"' + "," + '"' + jsn_val["url"] + '");')
        print('map.put("summary"' + "," + '"' + jsn_val["summary"] + '");')
        print('map.put("release"' + "," + '"' + jsn_val["release"] + '");')
        print('map.put("publisher"' + "," + '"' + jsn_val["publisher"] + '");')
        print('bookList.add(map);')
        print(' ')
        print(' ')
elif _SELECT_FLAG == 1:
    print('---------------------')
    print(jsn["id_99"])
    print('---------------------')

elif _SELECT_FLAG == 2:    
    jsn_str = json.dumps(jsn,indent=int(_INFO_SUM), ensure_ascii=False)
    print(jsn_str)

else :
    print("値が選択されていないか、実装されていません")
    