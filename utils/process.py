# coding=utf-8
from pymongo import *
import pandas as pd
import qiniu
import requests
import sys
from RedisQueue import RedisQueue as rq
import time

accessKey = "z1jgIomPPX9dpfQQur9IcKxAscXjXn1Of4KvqCgA"
secretKey = "wx-sSQb1FT2kiGRKilRgHk4IvCm_laFrDnT81_oh"
domain = "op9cfw6va.bkt.clouddn.com"


# 解析结果
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


# 无key上传，http请求中不指定key参数
def upload_without_key(bucket, filePath):
    # 生成上传凭证
    auth = qiniu.Auth(accessKey, secretKey)
    upToken = auth.upload_token(bucket, key=None)

    # 上传文件
    retData, respInfo = qiniu.put_file(upToken, None, filePath)

    # 解析结果
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
    # print(sys.argv[:])
    client = MongoClient('mongodb://123.207.189.77:27017/')
    client.fundata.authenticate("illidan", "stormrage", mechanism='SCRAM-SHA-1')
    db = client.fundata
    r = rq(host='123.206.231.182', port=6379, password='fundata')
    task_queue = 'queue:task'
    result_queue = 'queue:result'
    while True:
        item = r.get(task_queue)
        file_name, p_id, d_id = item.split('-')
        print(item)
        download_with_key(file_name, sys.argv[1])
        p = pd.read_csv("/%s/%s" % (sys.argv[1], file_name)).describe()

        with open('/%s/result.txt' % (sys.argv[1]), 'w+') as f:
            f.write(str(p))

        collection = db.pullRequestStatistics
        statistics = {"pullrequest_id": p_id}
        collection.insert(statistics)
        r.put(result_queue, '%s-%d-1' % (p_id, time.time()))
