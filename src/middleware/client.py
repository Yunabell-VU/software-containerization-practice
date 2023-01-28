import pymongo 
import os

mongo_url_local = "mongodb://admin:password@localhost:27017"
mongo_url_docker = "mongodb://admin:password@host.docker.internal:27017"
mongo_url_docker_compose = "mongodb://admin:password@mongodb"
mongo_url_k8s = "mongodb://{user}:{pwd}@{url}".format(user = os.environ['USER_NAME'], pwd = os.environ['USER_PWD'], url = os.environ['DB_URL'])

mongo_client = pymongo.MongoClient(mongo_url_k8s)