import requests
from lxml import etree  # 从lxml中导入etree
import time
import pymongo as pm

# 获取连接
client = pm.MongoClient('localhost', 27017)  # 端口号是数值型

# 连接目标数据库
db = client.sun

# 数据库用户验证
db.authenticate("dba", "dba")

headers = {
    "Host": "yglz.tousu.hebnews.cn",
    "Origin": "http://yglz.tousu.hebnews.cn"
}
try:
    response = requests.post("http://yglz.tousu.hebnews.cn/l-1001-5-")
    html = response.content.decode("utf-8")
except Exception as e:
    print(e)

tree=etree.HTML(html)  # 解析html

hids = tree.xpath('//input[@type="hidden"]')

common_param = {}

for ipt in hids:
    common_param.update({ipt.get("name"):ipt.get("value")})

for i in range(1,691):
    common_param.update({"__CALLBACKPARAM":f"Load|*|{i}",
                       "__CALLBACKID": "__Page",
                       "__EVENTTARGET":"",
                       "__EVENTARGUMENT":""})


    response = requests.post("http://yglz.tousu.hebnews.cn/l-1001-5-",data=common_param,headers=headers)
    html = response.content.decode("utf-8")
    print("*"*200)

    tree = etree.HTML(html)  # 解析html
    divs = tree.xpath('//div[@class="listcon"]')
    for div in divs:
        try:
            shouli = div.xpath('span[1]/p/a/text()')[0]  # 受理单位
            type = div.xpath('span[2]/p/text()')[0].replace("\n","")  # 投诉类型
            content = div.xpath('span[3]/p/a/text()')[0]  # 投诉内容
            datetime = div.xpath('span[4]/p/text()')[0].replace("\n","")  # 时间
            status = div.xpath('span[6]/p/text()')[0].replace("\n","")  # 时间
            one_data = {"shouli":shouli,
                        "type":type,
                        "content":content,
                        "datetime":datetime,
                        "status":status,
                        }
            print(one_data)
            db.wenzheng.insert_one(one_data)  # 插入单个文档
        except Exception as e:
            print("内部数据报错")
            print(div)
            continue
    print("数据插入成功{}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
    time.sleep(2)





