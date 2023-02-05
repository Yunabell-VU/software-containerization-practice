# README

## Application

### Class Diagram

![UML-cd](https://github.com/Yunabell-VU/containerization-group30/blob/presentation/demo/sc-class-diagram.png)

### Sequence Diagram

![UML-sd](https://github.com/Yunabell-VU/containerization-group30/blob/presentation/demo/sc-sequence-diagram.png)

---

## Prerequisites

1. `Docker`  installed
2. `microk8s` installed

**Notice:** All the demonstration are tested on Linux.

### Load Balancer


### Storage Class


### Image Registry


### Certificates

### Roles

### Network Policies

---

## Deployment

### Image build and Push

directory: `~/src/middleware`
```shell
# build webapp image
docker build -t reisafriche/python-api:v2 .

# push webapp image
docker build reisafriche/python-api:v2
```

directory: `~/src/client`
```shell
# build webapp image
docker build -t reisafriche/vue-app:v5-domain .

# push webapp image
docker build reisafriche/vue-app:v5-domain
```

### Deploy application

directory: root of project
```shell
# packge helm chart
helm package outlets/
```
```shell
# install helm chart
helm install outlets outlets-0.1.0.tgz
```
check helm deployment status
```shell
helm list
```

### Horizontal Scale
check pods before scaling:
```shell
kubectl get pods
```

Scale
```shell
kubectl scale deployment api --replicas=3
kubectl scale deployment outlets --replicas=3
```

check pods after scaling:
```shell
kubectl get pods
```

### Uninstall deployment
```shell
helm delete helm chart
```

check helm status:
```shell
helm list
```

---

## Upgrade & Re-deployment

###  Re-build

### Upgrade

#### Rollout

#### Canary update


---

> The following manual is for developers of this project

## Developer Guides

### Network Policy Testing

**DB only allow ingress from api:**

Create a testing pod, open the terminal of the pod
```shell
kubectl run test-$RANDOM --rm -i -t --image=alpine -- sh
```
Try to access the DB:
```shell
wget -qO- --timeout=2 http://mongo-service:27017
```
This should return time out. Use exit or crtl + d to quit.

Create a testing pod using the label which will be selected by the api selector:
```shell
kubectl run test-$RANDOM --rm -i -t --image=alpine --labels="app=api" -- sh
```

Try to access the DB:
```shell
wget -qO- --timeout=2 http://mongo-service:27017
```

This should return success.  

**API only allow egress to DB:**

Create a testing pod using the label which will be selected by the api selector:
```shell
kubectl run test-$RANDOM --rm -i -t --image=alpine --labels="app=api" -- sh
```

Try to access the DB:
```shell
wget -qO- --timeout=2 http://mongo-service:27017
```
This should return success.

Since the ingress rule for the frontend is all allowed, it is ideal to test egress rules using the frontend. Try to access the the frontend:
```shell
wget -qO- --timeout=2 http://outlets-service:8080
```
This should return time out.

**Frontend only allow egress to API:**

Create a testing pod using the label which will be selected by the frontend selector:
```shell
kubectl run test-$RANDOM --rm -i -t --image=alpine --labels="app=outlets" -- sh
```
Since the ingress rule for the frontend is all allowed, it is ideal to test egress rules using the frontend. Try to access the the frontend:
```shell
wget -qO- --timeout=2 http://outlets-service:8080
```
This should return time out.

Try to access the the API:
 ```shell
wget -qO- --timeout=2 http://api-service:5000
```
This should return success.
### Enabling Load Balancer

```shell
microk8s enable metallb
```
You will be asked to enter a range of free ip addresses for the LB to associate with services. For example, 20 private ip addresses are provided if entering:
```shell
10.50.100.5-10.50.100.25
```

Package and install the latest helm chart. Use the command to check whether load balancers are up and running:
```shell
kubectl get svc
---
NAME              TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
kubernetes        ClusterIP      10.152.183.1     <none>        443/TCP          3h55m
mongo-service     ClusterIP      10.152.183.50    <none>        27017/TCP        29m
outlets-service   LoadBalancer   10.152.183.100   10.50.100.5   8080:30814/TCP   29m
api-service       LoadBalancer   10.152.183.153   10.50.100.6   5000:31924/TCP   29m
```

Taking the outlets-service as an example, the service is now accessible from:
- cluster ip + cluster port (10.152.183.100:8080)
- node ip + node port (10.0.2.15:30814)
- external ip + cluster port (10.50.100.5:8080)

### Enabling TLS

Delete current helm chart and package a new one:
```shell
helm delete outlets
helm package outlets outlets
```

**Premise**: enable ingress and cert-manager

```shell
microk8s enable ingress
microk8s enable cert-manager
```

For the ingress to work locally without a proper DNS server setup, add the following to /etc/hosts:

```shell
127.0.0.1 my-webapp-group30.com
```

Install the helm chart:

```shell
helm install outlets outlets-0.1.0.tgz
```

Check tls related configurations:
```shell
kubectl get clusterissuer
---
NAME                        READY   AGE
selfsigned-cluster-issuer   True    42m -> the cluster issuer which creates a self-signed root certificate for facilitating a private CA
---


kubectl get issuer
---
NAME             READY   AGE
outlets-issuer   True    41m -> the private CA issuer which uses the root certificate to issue certificate for its residing namespace
---


kubectl get secret 
---
NAME                            TYPE                 DATA   AGE
root-ca-secret                  kubernetes.io/tls    3      90m -> place to store the self-signed root certificate 

my-ingress-cert                 kubernetes.io/tls    3      90m -> place to store the certificate issued by the private CA issuer
...
mongo-secret                    Oppaque              2      43m
sh.helm.release.v1.outlets.v1   helm.sh/release.v1   1      43m
```

**Related yaml fiels:**

selfsigned-cluster-issuer.yaml -> a self-signed cluster issuer

root-ca.yaml -> send request to the selfsigned-cluster-issuer to create a root certificate. The root certificate is stored in root-ca-secret.

outlets-issuer.yaml -> the issuer which sign the ingress certificate request using the root certificate

webapp-ingress.yaml -> send certificate request to the outlets-issuer to create a certificate for the webapp ingress. The certificate is stored in my-ingress-cert  

After all the workloads are up and running, check whether you can access the webapp via:
```shell
https://my-webapp-group30.com
```
Check whether http redirect works properly:
```shell
http://my-webapp-group30.com
```
Check whether api calls work properly:
```shell
https://my-webapp-group30.com/menus/price/above/50
```

And so on so forth...

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
// cai token
curl -X GET https://127.0.0.1:16443/api/v1/namespaces/default/pods --header "Authorization: Bearer 232OFLvMPANyomLteB2WTjs2I+yUjSVMJJyK4Lne///6gP1rCl2of4wo6OafG/Bq" --insecure
//200: OK

// cai token
curl -X GET https://127.0.0.1:16443/api/v1/namespaces/default/services --header "Authorization: Bearer 232OFLvMPANyomLteB2WTjs2I+yUjSVMJJyK4Lne///6gP1rCl2of4wo6OafG/Bq" --insecure
//403: FORBIDDEN

// yuna token
curl -X GET https://127.0.0.1:16443/api/v1/namespaces/default/services --header "Authorization: Bearer UdrysVbZvQj6J/oAUWeVT2FMyv4ut/tnydXhJdcL/MnuqvKhnNuf7CHgH2sDHCjA" --insecure
//200: OK

// yuna token
curl -X GET https://127.0.0.1:16443/api/v1/namespaces/default/secrets --header "Authorization: Bearer UdrysVbZvQj6J/oAUWeVT2FMyv4ut/tnydXhJdcL/MnuqvKhnNuf7CHgH2sDHCjA" --insecure
//403: FORBIDDEN

// fan token
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
To run other image or other variant in values versions:
```shell
helm install outlets outlets-0.1.0.tgz -f outlets/values-ssh.yaml
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
- External Service (NodePort) - API: **30020**
- External Service (NodePort) - WebApp: **30030**
---------------------------------------------------------------------------------------------------------------------

## Local version (Dev mode)

### Prerequisites

1. `Docker`  installed
2. `Python >= 3.4`  installed
3. `Node.js >= 16` installed

### 1. Run the database

#### Pull `MongoDb` official image from docker

Run the following command to pull MongoDB

```bash
$ docker pull mongo:4.4.6
```

#### Run database

Run the following command to create a container

```bash
$ docker run --name mongo -p 27017:27017 -d mongo

# "~/desktop/" can be replaced with the local path you want
```

**Notice**:  do not run the database in `--auth` mode

### 2. Run the API

#### Install required python modules

In your shell, enter the root directory, run the following command to install required modules (Flask, pymongo)

```bash
$ pip install -r requirements.txt

# or
$ pip3 install -r requirements.txt
```



#### Run the API

After successfully installed these modules, enter  directory `/src/middelware` , run the python file `run.py`

```bash
$ python3 run.py
```

**Notice**: Make sure your docker container mongodb is still running at `PORT:27017`

You should be able to see the following text:

#### Test API

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


#### Run the Web

Make sure Node.js (version >= 16) is installed.

**Keep API running, open a new terminal.**

Go to the directory `/src/client`, enter the following CMD in order:

```bash

$ npm install
$ npm run dev

```

Open the webpage shown in Local:
http://127.0.0.1:5173/ (by default)
