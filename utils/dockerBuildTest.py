import docker
import os

client = docker.DockerClient(base_url='tcp://192.168.11.108:2375')


def build_img(type):
    if type == 1:
        # process container
        return client.images.build(tag='process:v1', path=os.path.split(os.path.realpath(__file__))[0])
    elif type == 2:
        # jupyter container
        return client.images.build(tag='jupyter:v1', path=os.path.split(os.path.realpath(__file__))[0])


def create_container(type):
    if type == 1:
        return client.containers.create("process:v1", labels=['process'],
                                     detach=True, tty=True, volumes={'/tmp': {'bind': '/data', 'mode': 'rw'}})
    elif type == 2:
        return client.containers.create("jupyter:v1", labels=['jupyter'],
                                     detach=True, ttyll=True, volumes={'/tmp': {'bind': '/data', 'mode': 'rw'}})


def start_container(container, type, **kwargs):
    container.start()
    if type == 1:
        return container.exec_run('python /src/process.py %s data %d %d' % (
            kwargs['key'].encode('utf-8'), kwargs['pull_request_id'], kwargs['dataset_id']),)
    elif type == 2:
        return container.exec_run('python /src/process.py %s data %d %d' % (
            kwargs['key'].encode('utf-8'), kwargs['pull_request_id'], kwargs['dataset_id']),)


if __name__ == "__main__":
    # build_img(1)
    # c = create_container(1)
    # start_container(c, 1, key = u'o_1bgkh3g1n194p13dmrov1m6437j7.csv', pull_request_id=4 ,dataset_id=1)
    client = docker.DockerClient(base_url='tcp://192.168.11.108:2375')
    containers = client.containers.list(all=True, filters={'label':'process'})
    print containers
    for c in containers:
        print c.status