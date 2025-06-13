import json

import requests

from 飞书匿名登录0 import get_anonymous_session

cookies = {
    'session': get_anonymous_session(),
}

headers = {
    'authority': 'cits7vio8b.feishu.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'f-version': 'docs-6-3-1748932565147',
    'referer': 'https://cits7vio8b.feishu.cn/share/base/view/shrcn0T0NcS3UyFsOAMJqZ9GoeS',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

params = {
    'shareToken': 'shrcn0T0NcS3UyFsOAMJqZ9GoeS',
}
# https://ncnjv3qw5wjd.feishu.cn/share/base/view/shrcn0T0NcS3UyFsOAMJqZ9GoeS
response = requests.get(
    'https://cits7vio8b.feishu.cn/space/api/bitable/external/view/share/records_and_meta',
    params=params,
    cookies=cookies,
    headers=headers,
)
# print(response.text)
if response.status_code==200:
    jsonResult=response.json()
    if jsonResult["code"]==0:
        dataStr=jsonResult["data"]
        if dataStr:
            # print(dataStr)
            snapshot=dataStr['snapshot']
            snapshotJson = json.loads(snapshot)
            # print(snapshotJson)
            fieldMap=snapshotJson["fieldMap"]
            name1FieldName="fldQa0uO5U"
            name2FieldName="fldpe0gtNe"
            for fieldMapUItemKey,fieldMapUItemValue in dict(fieldMap).items():
                if fieldMapUItemValue["name"]=="name1":
                    name1FieldName=fieldMapUItemKey
                if fieldMapUItemValue["name"] == "name2":
                    name2FieldName = fieldMapUItemKey

            viewShareEntity=snapshotJson["viewShareEntity"]
            recordMap=viewShareEntity["recordMap"]
            # print(recordMap)
            for recordItem in dict(recordMap).values():
                name1Value=dict(recordItem[name1FieldName])
                name2Value=dict(recordItem[name2FieldName])
                if name1Value["value"] and name2Value["value"]:
                    # 要清空空格才对 或许还要添加混淆？？？ 先不吧 激活完毕就关闭
                    mac=dict(list(name1Value["value"])[0])["text"]
                    accode=dict(list(name2Value["value"])[0])["text"]
                    print(mac,accode)
    else:
        print("响应失败")
        print(response.json())

else:
    print("响应失败")
    print(response.json())


