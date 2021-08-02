import json
_DEBUG_FILE = 'Amazon2021.08.02-04-20.json' #出力したいjsonファイル


# Eclipse IDE専用プログラム出力


with open(_DEBUG_FILE, 'r', encoding='utf-8_sig') as f:
    jsn = json.load(f)



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

print('---------------------')
#print(jsn["id_99"])