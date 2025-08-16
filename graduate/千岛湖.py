import re
import requests
import json
import time
import csv

c = open(r'C:\Users\shino\Desktop\毕业论文\评论数据\千岛湖.csv', 'a+', newline='', encoding='utf-8')
fieldnames = ['user', 'time', 'score', 'content']
writer = csv.DictWriter(c, fieldnames=fieldnames)
writer.writeheader()

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}

#过滤消息头
postUrl = "https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList"

html = requests.post(postUrl, data=json.dumps(data_1)).text
html = json.loads(html)
jingqu = '千岛湖'
pages = html['data']['totalpage']
datas = []
for j in range(pages):
    data1 = {
			"channelType":2,
			"collapseType":0,
			"commentTagId":0,
			"pageIndex":1,
			"pageSize":10,
			"poiId":97470,
			"sourceType":1,
			"sortType":3,
				"starType":0
		"head":
			{
				"cid":"09031092215908133628",
				"ctok":"",
				"cver":"1.0",
				"lang":"01",
				"sid":"8888",
				"syscode":"09",
				"auth":"",
				"xsid":"",
				"extension": [
                {
                    "name": "protocal",
                    "value": "https"
                }
            ]
        },
        "ver": "7.10.3.0319180000"
    }
    datas.append(data1)

for k in datas[:2000]:
    print('正在抓取第' + k['pagenum'] + "页")
    time.sleep(3)
    html1 = requests.post(postUrl, data=json.dumps(k)).text
    html1 = json.loads(html1)
    comments = html1['data']['comments']

    for i in comments:
        user = i['uid']
        time1 = i['date']
        score = i['score']
        content = i['content']
        content = re.sub("&#x20;", "", content)
        content = re.sub("&#x0A;", "", content)

        writer.writerow({'user': user, 'time': time1, 'score': score, 'content': content})
c.close()
