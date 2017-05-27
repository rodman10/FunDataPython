import dockerBuildTest
import docker
import sqlite3


class DockerManagement(object):
    def __init__(self, c_size, j_size):
        self.calculate_pool, self.jupyter_pool = [], []
        self.c_size, self.j_size = c_size, j_size
        self.queue = []
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
        create_tb_cmd = 'CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, t_id TEXT, status TEXT, c_id TEXT, update_time INTEGER);'
        cursor.execute(create_tb_cmd)
        cursor.close()

        client = docker.DockerClient(base_url='tcp://192.168.11.108:2375')
        for event in client.events(filters={'label': "process"}):
            event = eval(event)
            cursor = conn.cursor()
            insert_dt_cmd = 'INSERT INTO logs (t_id, status, c_id,update_time) VALUES (?,?,?,?);'
            cursor.execute(insert_dt_cmd, (event['Actor']['Attributes']['name'], event['status'], event['id'], event['time']))
            cursor.close()
            conn.commit()
            print event
        conn.close()

            # def update_c_pool():
        #     containers = client.containers.list(all=True, filters={'label':'process'})
        #

    def acquire(self):
        if self.c_size > len(self.calculate_pool):
            c = dockerBuildTest.process()
            self.calculate_pool.append(c.id)

if __name__ == "__main__":
    DockerManagement(10, 10)