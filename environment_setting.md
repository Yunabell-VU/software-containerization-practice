# Environment Setting

## Prerequisites

1. `Docker`  installed
2. `Python >= 3.4`  installed

## 1. Run the database

### Pull `MongoDb` official image from docker

Run the following command to pull MongoDB

```bash
$ docker pull mongo
```

### Run database

Run the following command to create a container

```bash
$ docker run --name <YOUR-NAME> -p 8888:27017 -v /data/db:/data/db -d mongo
```

`--name <YOUR-NAME>` : name the container as you like.

**Notice**:  do not run the database in `--auth` mode


### Test connection

Run the following command to enter mongo shell

**Notice**: `<YOUR-NAME>` can be replaced by container id, use `$ docker ps` to inspect container id

```bash
$ docker exec -it <YOUR-NAME> mongo
```

If you see the following text, then the connection is a succeess.

>MongoDB shell version <v4.4.6>
>connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
>Implicit session: session { "id" : UUID("4516667f-0417-48b1-8d71-34376fe09bc9") }
>MongoDB server version: 4.4.6
>Welcome to the MongoDB shell.
>
>...

Exit the database

```bash
>> exit
```



## 2. Run the API

### Install required python modules

Run the following command to install `Flask` and `pymongo` , if you can not run the command, please make sure your version of python is at least 3.4

```bash
$ pip install flask
$ pip install pymongo
```

### Run the API

After successfully installed these modules, enter  directory `/dashmote_case_yc/project/src` , run the python file `run.py`

```bash
$ python run.py
```

**Notice**: Make sure your docker container mongodb is still running at `PORT:8888`



If `run.py` launched successfully, you should be able to see the following text:

> tripadvisor_out insert successfully
> tripadvisor_user insert successfully
> tripadvisor_reviews insert successfully
> ubereats_out insert successfully
> ubereats_menu insert successfully
>
>  * Serving Flask app 'api' (lazy loading)
>  * Environment: production
>    WARNING: This is a development server. Do not use it in a production deployment.
>    Use a production WSGI server instead.
>  * Debug mode: off
>  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
>  * ...



### Test API

Open your browser at 

`http://127.0.0.1:5000/` 

or `http://localhost:5000/`

 you should be able to see the introduction page.



Here is the list of API provided:

| API                           | Description                                      | Method | Example                                   |
| :---------------------------- | :----------------------------------------------- | :----: | :---------------------------------------- |
| /                             | Index page                                       |  GET   | localhost:5000/                           |
| /outlets/brand/[brand name]   | List outlets which have a certain brand.         |  GET   | localhost:5000/outlets/brand/fuz          |
| /outlets/source/[source name] | List outlets by their source                     |  GET   | localhost:5000/outlets/source/ubereats    |
| /menus/price/above/[price]    | List menus which the item is above certain price |  GET   | localhost:5000/menus/price/above/10       |
| /insert/outlet/[data]         | Add a new outlet into the database               |  POST  | localhost:5000/insert/outlet/?name = ''.. |

