import docker
import os

def process(key, pull_request_id, dataset_id):
    client = docker.DockerClient(base_url='tcp://192.168.11.108:2375')
    img = client.images.build(tag='process:v1', path=os.path.split(os.path.realpath(__file__))[0])
    client.containers.run("process:v1", '%s data %d %d' % (key.encode('utf-8'), pull_request_id, dataset_id), remove=True, volumes={'/tmp': {'bind': '/data', 'mode': 'rw'}})
    print 'success'

if __name__ == "__main__":
    process(u'o_1bgkh3g1n194p13dmrov1m6437j7.csv', 1 ,1)