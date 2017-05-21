#coding=utf-8

import qiniu
import requests
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
    with open(path+'/'+key,'w+') as f:
        f.write(r.content)
    assert r.status_code == 200


def main():
    bucket = "test"
    filePath = "/home/huang/Pictures/Wallpapers/341558.jpg"
    # upload_without_key(bucket, filePath)
    download_with_key("FhF3mdqcm36Ocw7rvSBwO58OIvvJ", '/')

if __name__ == "__main__":
    main()
