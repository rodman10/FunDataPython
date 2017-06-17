# coding=utf-8
from pymongo import *
import pandas as pd
import qiniu
import requests
import sys
from RedisQueue import RedisQueue as rq
import time
import os

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


# 有key上传，http请求中指定key参数
def upload_with_key(bucket, filePath, key):
    # 生成上传凭证
    auth = qiniu.Auth(accessKey, secretKey)
    upToken = auth.upload_token(bucket, key=key)

    # 上传文件
    retData, respInfo = qiniu.put_file(upToken, key, filePath)

    # 解析结果
    parseRet(retData, respInfo)


def download_with_key(key, path, dataset_id):
    auth = qiniu.Auth(accessKey, secretKey)
    base_url = 'http://%s/%s' % (domain, key)
    private_url = auth.private_download_url(base_url)
    r = requests.get(private_url)
    os.mkdir('/%s/dataset_%s' % (path, dataset_id))
    with open('/%s/dataset_%s/%s' % (path, dataset_id, key),'wb+') as f:
        f.write(r.content)
    assert r.status_code == 200


# arg1 filename arg2 filepath arg3 pull_id arg4 datasetId
if __name__ == "__main__":
    # print(sys.argv[:])
    client = MongoClient('mongodb://123.207.189.77:27017/')
    client.fundata.authenticate("illidan", "stormrage", mechanism='SCRAM-SHA-1')
    db = client.fundata
    r = rq(host='123.206.231.182', port=6379, password='fundata')
    merge_queue = 'queue:merge'
    result_queue = 'queue:result'
    for item in r.listen(merge_queue):
        item = r.get(merge_queue)
        new_name, main_name, d_id = item.split('-')
        download_with_key(new_name, sys.argv[1], d_id)
        download_with_key(main_name, sys.argv[1], d_id)
        ####################################################
        # merge operate                                    #
        # return value: file_path                          #
        ####################################################
        upload_with_key("fundata", "", main_name)