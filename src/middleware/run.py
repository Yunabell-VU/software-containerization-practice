from api import app
from parse import j2m
from client import mongo_client

if __name__ == '__main__':
    if mongo_client.container_group30 is None:
        j2m.sample_to_database() 
    app.run(host="0.0.0.0", port =5000, debug=False)