There are 3 directories that represents the 3 microservices:

1) ponpluse:
represesnts the microservice with the API, the files are:
1.1) pondpulse-app.py:
represesnts the applications that will run in the container for the pondpulse microservice,
it based on flask framework for python
1.2) ponpluse-deployment.yaml:
represent the yaml file that will be deployed to the k8s cluser for the pondpulse microservice
1.3) pondpulse-dockerfile:
represents the dockerfile that will creates the docker image for pondpulse service, it will be pushed to
repository in dockerhub with tag saeedazem93/pondpulse-image:latest
1.4) pondpulse-lb.yaml:
will creates load balancer for pondpulse microservice so it could be access oustise the k8s cluster
1.5) pondpulse-service:
will creates the clusterIP service for pondpulse microservice so it could be access inside the k8s cluster
1.6) requirements.txt:
Includes any needed packages specified to be installed in the pondpulse docker image

2) flytrap:
represesnt the microservice that will connect to pondpulse API and make changes in its data, the files are:
2.1) flytrap-app.py:
represesnts the applications that will run in the container for the flytrap microservice, based on python code
2.2) flytrap-deployment.yaml:
represent the yaml file that will be deployed to the k8s cluser for the flytrap microservice
2.3) flytrap-dockerfile:
represents the dockerfile that will creates the docker image for flytrap service, it will be pushed to
repository in dockerhub with tag saeedazem93/flytrap-image:latest
2.4) requirements.txt:
Includes any needed packages specified to be installed in the flytrap docker image

3) dbribbit:
represesnt the microservice that will connect to pondpulse API and pull data from it and save it to db, the files are:
3.1) dbribbit-app.py:
represesnts the applications that will run in the container for the db microservice, based on python code and it will create an sqllite db with name dbribbit.db Includes
table called faulty_versions
3.2) dbribbit-dockerfile:
represents the dockerfile that will creates the docker image for dbribbit service, it will be pushed to
repository in dockerhub with tag saeedazem93/dbribbit-image:latest
3.3) requirements.txt:
Includes any needed packages specified to be installed in the dbribbit docker image

===============

example for creation of docker image for pondpulse microservice(others are the same):
1) go to pondpulse folder and run the command:
docker build -t pondpulse-image -f pondpulse-dockerfile .
2) create local tag saeedazem93/pondpulse-image:
docker tag pondpulse-image saeedazem93/pondpulse-image
3) push image to dockerhub container registry:
docker push saeedazem93/pondpulse-image

=====================

How to Create the microseriveces in k8s cluster:
1) go to pondpulse folder and run the command:
"kubectl apply -f ."
it should print the message:
deployment.apps/pondpulse-deployment created
service/pondpulse-lb-service created
service/pondpulse-service created
notes: 
1.1) it will creates a pod with suffix name pondpulse-deployment-* for example: pondpulse-deployment-794975469f-pdc9l,
you could see it by running the commad "kubectl get po"
1.2) it will creates a ClusterIP service for pondpulse with name "pondpulse-service",
you could see it by running the command "kubectl get svc"
1.3) it will creates a load balancer service for pondpulse with name "pondpulse-lb-service",
you could see it by running the command "kubectl get svc"

2) go to flytrap folder and run the command:
"kubectl apply -f ."
it should print the message:
deployment.apps/flytrap-deployment created
notes:
2.1) it will creates a pod with suffix name flytrap-deployment-* for example: flytrap-deployment-74457fd589-vfpf6,
you could see it by running the commad "kubectl get po"

3) go to dbribbit folder and run the command:
"kubectl apply -f ."
it should print the message:
deployment.apps/dbribbit-deployment created
3.1) it will creates a pod with suffix name dbribbit-deployment-* example: dbribbit-deployment-57f8df9f5f-lzqbz,
you could see it by running the commad "kubectl get po"

==================

to check if the microservices are working you should:
1) run the command "kubectl logs <pod-name>" for each microservice and see in the logs that's it's running

1.1)for example logs for pondpulse ms: "kubectl logs pondpulse-deployment-794975469f-pdc9l"
INFO:PondPulse:Updated state of Frog5 to insecure
INFO:werkzeug:10.0.102.199 - - [26/Sep/2023 18:36:24] "PUT /microservices/Frog5 HTTP/1.1" 200 -

1.2) example logs for flytrap ms:
INFO:FlyTrap:Updated state of Frog5 to slow

1.3) example logs for dbribbit ms:
INFO:root:Insert into table faulty_versions in dbribbit.db (microservice_name, version, state) with Values: (Frog5, 1, insecure)

2) copy the "EXTERNAL-IP" of the load balancer(you can get it by running the command "kubectl get svc") and run it in the browser,
you shoud get the output "PondPulse Microservice"

3) continue from last step and add "/microservices" to the end of the "EXTERNAL-IP" URL,
it should display all data about the 5 Frogs, for example(this is the init state of data):
{
  "Frog1": {
    "state": "healthy",
    "version": 1
  },
  "Frog2": {
    "state": "healthy",
    "version": 1
  },
  "Frog3": {
    "state": "healthy",
    "version": 1
  },
  "Frog4": {
    "state": "healthy",
    "version": 1
  },
  "Frog5": {
    "state": "healthy",
    "version": 1
  }
}


4) if flytrap microservice is working the state of each Frog shoud be modifed to inscure or slow, for example:
{
  "Frog1": {
    "state": "slow",
    "version": 1
  },
  "Frog2": {
    "state": "slow",
    "version": 1
  },
  "Frog3": {
    "state": "insecure",
    "version": 1
  },
  "Frog4": {
    "state": "insecure",
    "version": 1
  },
  "Frog5": {
    "state": "insecure",
    "version": 1
  }
}
