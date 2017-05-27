import docker
import os


def process(key, pull_request_id, dataset_id):
    client = docker.DockerClient(base_url='tcp://192.168.11.108:2375')
    img = client.images.build(tag='process:v1', path=os.path.split(os.path.realpath(__file__))[0])
    return client.containers.run("process:v1", '%s data %d %d' % (key.encode('utf-8'), pull_request_id, dataset_id),
                                 labels=['process'], name='-'.join((str(pull_request_id), str(dataset_id))), detach=True, volumes={'/tmp': {'bind': '/data', 'mode': 'rw'}})

if __name__ == "__main__":
    process(u'o_1bgkh3g1n194p13dmrov1m6437j7.csv', 4 ,1)
    client = docker.DockerClient(base_url='tcp://192.168.11.108:2375')
    containers = client.containers.list(all=True, filters={'label':'process'})
    print containers
    for c in containers:
        print c.status