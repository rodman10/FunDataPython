from utils import docker_builder as db

df = db.DockerFactory()
img = df.build_img(1)
df.run_container(1, dir="dataset_1", user_id=1, port=7001)

