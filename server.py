from wsgiref.simple_server import make_server
import os
from pathlib import Path
import json

_DEBUG_PRINT = 1
_DEBUG_FILE = '' #出力したいjsonファイル
_INFO_SUM = 10 #インデントに設定をする要素数
_SELECT_FLAG = 99 # 0,1,2,3

p = Path(".")
files = files = list(p.glob("./*.json"))
file_updates = {file_path: os.stat(file_path).st_mtime for file_path in files}
newst_file_path = max(file_updates, key=file_updates.get)
_DEBUG_FILE = str(newst_file_path)

if _DEBUG_PRINT==1:
    print(_DEBUG_FILE)

with open(_DEBUG_FILE, 'r', encoding='utf-8_sig') as f:
    jsn = json.load(f)

 
 
def app(environ, start_response):
  status = '200 OK'
  headers = [
    ('Content-type', 'application/json; charset=utf-8'),
    ('Access-Control-Allow-Origin', '*'),
  ]
  start_response(status, headers)
 
  return [json.dumps(jsn, indent=int(_INFO_SUM), ensure_ascii=False).encode("utf-8")]
 
with make_server('', 3000, app) as httpd:
  print("Serving on port 3000...")
  httpd.serve_forever()
