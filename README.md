# README

## Prerequisites

1. `Docker`  installed
2. `Python >= 3.4`  installed
3. `Node.js >= 16` installed



## Temprorary Guides

### Buid Docker network

**In your terminal (make sure docker is launched):**
```bash
docker network create task-net

docker run --name=mongo --rm -d --network=task-net mongo

docker run --name=app-server --rm -p 5000:5000 -d --network=task-net reisafriche/test:1.0.3

docker run --name=app-client --rm -p 8080:8080 -d --network=task-net reisafriche/vue-app:1.0.0  
```

**Test**

open: http://localhost:8080

---------------------------------------------------------------------------------------------------------------------

## 1. Run the database

### Pull `MongoDb` official image from docker

Run the following command to pull MongoDB

```bash
$ docker pull mongo:4.4.6
```

### Run database

Run the following command to create a container

```bash
$ docker run --name mongodb -p 8888:27017 -v ~/desktop/data/db:/data/db -d mongo

# "~/desktop/" can be replaced with the local path you want
```

**Notice**:  do not run the database in `--auth` mode



<!-- ### Test connection

> This part does not functioning well at the moment, please skip it! Go to the section Run the API

Run the following command to enter mongo shell

**Notice**: container name `mongo` can be replaced by container id, use `$ docker ps` to inspect container id

```bash
$ docker exec -it mongodb mongo
```

If you see the following text, then the connection is a succeed.

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
 -->


## 2. Run the API

### Install required python modules

In your shell, enter the root directory, run the following command to install required modules (Flask, pymongo)

```bash
$ pip install -r requirements.txt

# or
$ pip3 install -r requirements.txt
```



### Run the API

After successfully installed these modules, enter  directory `/src/middelware` , run the python file `run.py`

```bash
$ python3 run.py
```

**Notice**: Make sure your docker container mongodb is still running at `PORT:8888`

You should be able to see the following text:

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

or `http://localhost:5000/`,

 you should be able to see the introduction page.



Here is the list of API provided:

| API                           | Description                                                  | Method | Example                                           |
| :---------------------------- | :----------------------------------------------------------- | :----: | :------------------------------------------------ |
| /                             | Index page                                                   |  GET   | 127.0.0.1:5000/                                   |
| /outlets/brand/<brand name>   | List outlets which have certain brand. You can enter only the first several letters of a brand, e.g. 'coca' for 'Coca-Cola'. Here is some examples of brand in the database: 'Fuze Tea', 'Frnandes', 'Chaudfontaine', etc. You don't need to capitalize the brand name. |  GET   | 127.0.0.1:5000/outlets/brand/fuz                  |
| /outlets/source/<source name> | List outlets by their source                                 |  GET   | 127.0.0.1:5000/outlets/source/ubereats            |
| /menus/price/above/<price>    | List menus which the item is above certain price             |  GET   | 127.0.0.1:5000/menus/price/above/10               |
| /insert/outlet/<data>         | Add a new outlet into the database                           |  POST  | 127.0.0.1:5000/insert/outlet/?id_outlet=......... |


### Run the Web

Make sure Node.js is installed.

Go to the directory `/src/client`, enter the following CMD in order:

```bash

$ npm install
$ npm run dev

```

Open the webpage shown in Local:
http://127.0.0.1:5173/ (by default)
