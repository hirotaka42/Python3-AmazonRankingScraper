from wsgiref.simple_server import make_server
import json
_DEBUG_FILE = 'Amazon2021.08.04-09-41.json' #出力したいjsonファイル
# Eclipse IDE専用プログラム出力
_INFO_SUM = 10

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
