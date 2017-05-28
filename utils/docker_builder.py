import docker
import os


class DockerFactory(object):
    def __init__(self):
        self.client = docker.DockerClient(base_url='tcp://192.168.11.108:2375')
        self.img_tags = ['process:v1', 'jupyter:v1']
        self.img_labels = ['process', 'jupyter']

    def build_img(self, img_id):
        # process container or jupyter container
        return self.client.images.build(tag=self.img_tags[img_id], path=os.path.split(os.path.realpath(__file__))[0])

    def run_container(self, img_id, ):
        if img_id == 0:
            return self.client.containers.run(self.img_tags[img_id], 'data', labels=[self.img_labels[img_id]],
                                              detach=True, volumes={'/tmp': {'bind': '/data', 'mode': 'rw'}})

    def run_containers(self, num, img_id,):
        c_list = []
        for i in range(num):
            c_list.append(self.run_container(img_id))
        return c_list

if __name__ == "__main__":
    df = DockerFactory()
    df.build_img(0)
    c = df.run_container(0)
    # t = start_container(c, 1, key=u'o_1bgkh3g1n194p13dmrov1m6437j7.csv', pull_request_id=4 ,dataset_id=1)
    # for i in t:
    #     print i

    client = docker.DockerClient(base_url='tcp://192.168.11.108:2375')
    containers = client.containers.list(all=True, filters={'label':'process'})
    print containers
    for c in containers:
        print c.status