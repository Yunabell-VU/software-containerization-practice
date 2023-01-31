# README

## Prerequisites

1. `Docker`  installed
2. `Python >= 3.4`  installed
3. `Node.js >= 16` installed



## Temprorary Guides

### Authentication through bearer token (Microk8s)

Method: edit the known_tokens.csv

Default known_tokens.csv directory (for Microk8s):

```shell
/var/snap/microk8s/current/credentials/known_tokens.csv
```

**Make sure the hostname of the node contain no capital letter and underscore (_), then enable RBAC with:**

```shell
microk8s enable rbac
```

Append the following tokens to the end of the known_tokens.csv. This will add 3 users (fan, yuna, cai) to the k8s cluster (in the format of token, user, uid, "optional group name")

```shell
VxERUA62RoXUBcP0EDHtEI8YRJXRbMpS2eXm6NrjC1cmkkjedZmiGzKq4ctxu1Gz,fan,fan-id
UdrysVbZvQj6J/oAUWeVT2FMyv4ut/tnydXhJdcL/MnuqvKhnNuf7CHgH2sDHCjA,yuna,yuna-id
232OFLvMPANyomLteB2WTjs2I+yUjSVMJJyK4Lne///6gP1rCl2of4wo6OafG/Bq,cai,cai-id
```
Delete current helm chart and package a new one:
```shell
helm delete outlets
helm package outlets outlets
```

Reboot Microk8s:

```shell
microk8s stop
microk8s start
```

Install the helm chart and play with the *-role.yaml files in the templates. 

```shell
helm install outlets outlets-0.1.0.tgz
```

Check whether RBAC works as expected. The current RBAC structure has 2 roles, 1 clusterrole, and 3 rolebindings. Different level of permission to access resources are granted to the 3 users.

Some RBAC related instructions:
```shell
kubectl get role
kubectl get clusterrole
kubectl get rolebinding
kubectl get clusterrolebinding
```

Expected behavior using auth cai-i command:
```shell
kubectl auth can-i get pod --namespace default --as cai
//yes
kubectl auth can-i get services --namespace default --as cai
//no
kubectl auth can-i get services --namespace default --as yuna
//yes
kubectl auth can-i get secret --namespace default --as yuna
//no
kubectl auth can-i get secret --namespace default --as fan
//yes
kubectl auth can-i get secret --namespace default --as nobody
//no
```
The RBAC system can also be tested through requesting the k8s api-server.

Get the IP address for server:
```shell
kubectl config view | grep server
//server: https://127.0.0.1:16443
```

Expected behavior using api-server request:
```shell
// cai's token
curl -X GET https://127.0.0.1:16443/api/v1/namespaces/default/pods --header "Authorization: Bearer 232OFLvMPANyomLteB2WTjs2I+yUjSVMJJyK4Lne///6gP1rCl2of4wo6OafG/Bq" --insecure
//200: OK

// cai's token
curl -X GET https://127.0.0.1:16443/api/v1/namespaces/default/services --header "Authorization: Bearer 232OFLvMPANyomLteB2WTjs2I+yUjSVMJJyK4Lne///6gP1rCl2of4wo6OafG/Bq" --insecure
//403: FORBIDDEN

// yuna's token
curl -X GET https://127.0.0.1:16443/api/v1/namespaces/default/services --header "Authorization: Bearer UdrysVbZvQj6J/oAUWeVT2FMyv4ut/tnydXhJdcL/MnuqvKhnNuf7CHgH2sDHCjA" --insecure
//200: OK

// yuna's token
curl -X GET https://127.0.0.1:16443/api/v1/namespaces/default/secrets --header "Authorization: Bearer UdrysVbZvQj6J/oAUWeVT2FMyv4ut/tnydXhJdcL/MnuqvKhnNuf7CHgH2sDHCjA" --insecure
//403: FORBIDDEN

// fan's token
curl -X GET https://127.0.0.1:16443/api/v1/namespaces/default/secrets --header "Authorization: Bearer VxERUA62RoXUBcP0EDHtEI8YRJXRbMpS2eXm6NrjC1cmkkjedZmiGzKq4ctxu1Gz" --insecure
//200: OK

// unknown token
curl -X GET https://127.0.0.1:16443/api/v1/namespaces/default/secrets --header "Authorization: Bearer VxERUA62RoXUBcP0EDHtEI8YRJXRbMpS2eXm6NrjC1cmkkjedZmiGzKq4ctxu1Ga" --insecure
//401: UNAUTHORIZED
```

### Helm Chart

**IMPORTANT: clear your kubenetes resouces first, including configmap and secret!!**
```shell
kubectl delete all --all --namespace default
kubectl delete configmap mongo-config -n default
kubectl delete secret mongo-secret -n default
```

Install helm chart: https://helm.sh/

Mac:
```shell
brew install helm
```

Linux:
```shell
sudo snap install helm --classic
```


**To run the deployment:**  

At project root directory: (DEFAULT version)
```shell
helm install outlets outlets-0.1.0.tgz
```
(TO 小蔡：)To run other image or other variant in values versions:
```shell
helm install outlets outlets-0.1.0.tgz -f outlets/values-cai.yaml
```

**IF return errors such as localhost refuse to be connected, enter cmd below, and helm install again**
```shell
kubectl config view --raw > ~/.kube/config
microk8s kubectl config view --raw > ~/.kube/config
```

check if k8s is deployed:
```shell
kubectl get all
```
Notice, if your terminal does not display anything, kill it and launch a new terminal.

**To delete the deployment:**
```shell
helm delete outlets
```

Now check your k8s, all deployment should be gone!

**Any new yaml file can be throw into /app/templates folder**

**To pack new Helm Chart**  

At project root directory
```shell
helm package outlets outlets
```

**Play around and enjoy!!**


-------

### Test in k8s


> USE microk8s instead of minikube, unless you know how to enter minikube's virtual machine

Start microk8s
```shell
microk8s start
```

test if kubenetes works
```shell
kubectl get pod
```

At the root of /containerization-group30
```shell
# please apply the yaml files in order!!
kubectl apply -f mongo.yaml
kubectl apply -f api.yaml
kubectl apply -f frontend.yaml
```

Check pods:
```shell
kubectl get pod
```

Check services:
```shell
kubectl get svc
```

Check logs of pod:
```shell
kubectl logs <podName>
```

**TEST API**
use the CLUSTER-IP of `backend-service`, e.g.: 10.152.183.160  

open browser with the address: 
```shell
<ip_address>:5000
```

**TEST Frontend**
use the CLUSTER-IP of `frontend-service`, e.g.: 10.152.183.35  

open browser with the address:
```shell
<ip_address>:8080
```


----
(not neccessary) Find k8s ip:
```shell
kubectl get node -o wide
```

(To re-deploy) Delete all pods and resources:
```shell
kubectl delete all --all --namespace default
```

-----------------

### Buid Docker network (OUTDATED!!!!)

**In your terminal (make sure docker is launched):**
```bash
docker network create task-net

docker run --name=mongo --rm -d --network=task-net mongo

docker run --name=app-server --rm -p 5000:5000 -d --network=task-net reisafriche/python-api:1.0.0

docker run --name=app-client --rm -p 8080:8080 -d --network=task-net reisafriche/vue-app:1.0.2  
```

**Test**

open: http://localhost:8080


---------------------------------------------------------------------------------------------------------------------

## PORT

- MongoDB: **27017**
- API: **5000**
- WebAPP: **8080**
- External Service (NodePort): 30030
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
$ docker run --name mongo -p 27017:27017 -d mongo

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

**Notice**: Make sure your docker container mongodb is still running at `PORT:27017`

You should be able to see the following text:

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

Make sure Node.js (version >= 16) is installed.

**Keep API running, open a new terminal.**

Go to the directory `/src/client`, enter the following CMD in order:

```bash

$ npm install
$ npm run dev

```

Open the webpage shown in Local:
http://127.0.0.1:5173/ (by default)
