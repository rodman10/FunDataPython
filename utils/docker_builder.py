import docker
import os
import JupyterProxy as jp
from notebook.auth import passwd


class DockerFactory(object):
    def __init__(self):
        self.client = docker.DockerClient(base_url='tcp://123.207.189.77:2375')
        self.img_tags = ['process:v1', 'jupyter:v1', 'merge:v1']
        self.img_labels = ['process', 'jupyter', 'merge']
        self.port_set = set()
        self.proxies = {}

    def build_img(self, img_id):
        # process container or jupyter container
        cur_dir = os.path.split(os.path.realpath(__file__))[0]
        if img_id == 0:
            return self.client.images.build(tag=self.img_tags[img_id],
                                            path=cur_dir)
        elif img_id == 2:
            f = open(cur_dir+"/Dockerfile1")
            return self.client.images.build(tag=self.img_tags[img_id],
                                            dockerfile=cur_dir+"/Dockerfile1",
                                            path=cur_dir)
        else:
            f = open(cur_dir+"/JupyterDockerfile")
            return self.client.images.build(tag=self.img_tags[img_id],
                                            fileobj=f)

    def get_port(self):
        for i in range(7000, 7500):
            if i not in self.port_set:
                self.port_set.add(i)
                return i

    def configure_jupyter(self, user_id, dataset_id, port, img_id):
        jp.JupyterProxy().get_terminal(user_id, port)
        pwd = '19951116'
        hash = passwd(pwd)

        return self.client.containers.run(self.img_tags[img_id], '''
                                        --port=8888 
                                        --allow-root
                                        --NotebookApp.base_url=\"/jupyter/%s\" 
                                        --NotebookApp.base_project_url= \"/notebook\" 
                                        --NotebookApp.password=%s
                                        ''' % (user_id, hash),
                                          labels=[self.img_labels[img_id]],
                                          ports={'8888/tcp': port},
                                          detach=True,
                                          volumes={'/home/fundata/dataset_%s' % (dataset_id): {'bind': '/notebook',
                                                                                               'mode': 'rw'}})

    def run_container(self, img_id, **kwargs):
        if img_id != 1:
            return self.client.containers.run(self.img_tags[img_id], 'data',
                                              labels=[self.img_labels[img_id]],
                                              detach=True,
                                              volumes={'/home/fundata': {'bind': '/data', 'mode': 'rw'}})
        else:
            user_id = kwargs.get('user_id')
            dataset_id = kwargs.get('dataset_id')
            if dataset_id not in self.proxies:
                port = self.get_port()
                self.proxies[dataset_id] = {user_id: port}
                return self.configure_jupyter(user_id, dataset_id, port, img_id)
            else:
                if user_id not in self.proxies.get(dataset_id):
                    port = self.get_port()
                    self.proxies.get(dataset_id)[user_id] = port
                    return self.configure_jupyter(user_id, dataset_id, port, img_id)
                else:
                    return None

    def run_containers(self, num, img_id,):
        c_list = []
        for i in range(num):
            c_list.append(self.run_container(img_id))
        return c_list

if __name__ == "__main__":
    df = DockerFactory()
    df.build_img(0)
    c = df.run_container(0)
    # JupyterDockerfile = start_container(c, 1, key=u'o_1bgkh3g1n194p13dmrov1m6437j7.csv', pull_request_id=4 ,dataset_id=1)
    # for i in JupyterDockerfile:
    #     print i

    client = docker.DockerClient(base_url='tcp://123.207.189.77:2375')
    containers = client.containers.list(all=True, filters={'label':'process'})
    print containers
    for c in containers:
        print c.status