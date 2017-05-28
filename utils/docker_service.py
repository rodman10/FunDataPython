from docker_builder import DockerFactory
from RedisQueue import RedisQueue as rq
import sqlite3


class DockerManagement(object):
    def __init__(self, c_size=100, j_size=100):
        self.calculate_pool, self.jupyter_pool = None, None
        self.c_size, self.j_size = c_size, j_size
        self.queue = []
        self.r = rq(host='123.206.231.182', port=6379, password='fundata')

    def start(self):
        df = DockerFactory()
        df.build_img(0)
        self.calculate_pool = df.run_containers(self.c_size, 0)
        conn = sqlite3.connect('docker_log')
        cursor = conn.cursor()
        # try:
        #     create_tb_cmd = '''''
        #        CREATE TABLE IF NOT EXISTS logs
        #        (id TEXT,
        #        time INTEGER);
        #        '''
        #     conn.execute(create_tb_cmd)
        # except:
        #     print "Create table failed"
        create_tb_cmd = 'CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, p_id INTEGER , status INTEGER , update_time INTEGER);'
        cursor.execute(create_tb_cmd)
        cursor.close()

        while True:
            item = self.r.get('queue:result')
            print item
            cursor = conn.cursor()
            p_id, update_time, status = item.split('-')
            insert_dt_cmd = 'INSERT INTO logs (status, p_id, update_time) VALUES (?,?,?);'
            cursor.execute(insert_dt_cmd, (status, p_id, update_time))
            cursor.close()
            conn.commit()

        # client = docker.DockerClient(base_url='tcp://192.168.11.108:2375')
        # for event in client.events(filters={'label': "process"}):
        #     event = eval(event)
        #     cursor = conn.cursor()
        #     # if event['status'] == 'die':
        #     #     p = self.queue.pop()
        #     #     dockerBuildTest.start_container()
        #     insert_dt_cmd = 'INSERT INTO logs (t_id, status, c_id,update_time) VALUES (?,?,?,?);'
        #     cursor.execute(insert_dt_cmd, (event['Actor']['Attributes']['name'], event['status'], event['id'], event['time']))
        #     cursor.close()
        #     conn.commit()
        #     print event

            # def update_c_pool():
        #     containers = client.containers.list(all=True, filters={'label':'process'})
        #
    # def add_process_task(self, request):
    #     self.queue.append(request)
    #
    # def acquire(self):
    #     if self.c_size > len(self.calculate_pool):
    #         c = docker_builder.process()
    #         self.calculate_pool.append(c.id)

if __name__ == "__main__":
    dm = DockerManagement(1, 1)
    dm.start()