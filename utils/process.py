#coding=utf-8
from pymongo import *
import pandas as pd
import qiniu
import requests
import sys


accessKey = "z1jgIomPPX9dpfQQur9IcKxAscXjXn1Of4KvqCgA"
secretKey = "wx-sSQb1FT2kiGRKilRgHk4IvCm_laFrDnT81_oh"
domain = "op9cfw6va.bkt.clouddn.com"

#解析结果
def parseRet(retData, respInfo):
    if retData != None:
        print("Upload file success!")
        print("Hash: " + retData["hash"])
        print("Key: " + retData["key"])

        #检查扩展参数
        for k, v in retData.items():
            if k[:2] == "x:":
                print(k + ":" + v)

        #检查其他参数
        for k, v in retData.items():
            if k[:2] == "x:" or k == "hash" or k == "key":
                continue
            else:
                print(k + ":" + str(v))
    else:
        print("Upload file failed!")
        print("Error: " + respInfo.text_body)


#无key上传，http请求中不指定key参数
def upload_without_key(bucket, filePath):
    #生成上传凭证
    auth = qiniu.Auth(accessKey, secretKey)
    upToken = auth.upload_token(bucket, key=None)

    #上传文件
    retData, respInfo = qiniu.put_file(upToken, None, filePath)

    #解析结果
    parseRet(retData, respInfo)


def download_with_key(key, path):
    auth = qiniu.Auth(accessKey, secretKey)
    base_url = 'http://%s/%s' % (domain, key)
    private_url = auth.private_download_url(base_url)
    r = requests.get(private_url)
    with open('/' + path+'/'+key,'wb+') as f:
        f.write(r.content)
    assert r.status_code == 200

# arg1 filename arg2 filepath arg3 pull_id arg4 datasetId
if __name__ == "__main__":
    print(sys.argv[:])
    download_with_key(sys.argv[1], sys.argv[2])
    p = pd.read_csv("/%s/%s" % (sys.argv[2], sys.argv[1])).describe()

    with open('/%s/result.txt' % (sys.argv[2]), 'w+') as f:
        f.write(str(p))
    client = MongoClient('mongodb://123.207.189.77:27017/')
    client.fundata.authenticate("illidan", "stormrage", mechanism='SCRAM-SHA-1')
    db = client.fundata
    collection = db.pullRequestStatistics
    statistics = {"pullrequest_id": sys.argv[3]}
    collection.insert(statistics)
