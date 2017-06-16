# from utils import docker_builder as db
#
# df = db.DockerFactory()
# img = df.build_img(1)
# df.run_container(1, dataset_id=1, user_id=2)

from pymongo import *
client = MongoClient('mongodb://123.207.189.77:27017/')
client.fundata.authenticate("illidan", "stormrage", mechanism='SCRAM-SHA-1')
db = client.fundata

ds = db.datasetMeta.find_one({"dataset_id" : 1})
print ds["expressions"]