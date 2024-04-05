#!/bin/bash

minikube docker-env
eval $(minikube -p minikube docker-env)

cd ../WebApp
docker build -t web-app:latest .
docker save web-app | (eval $(minikube docker-env) && docker load)

cd ../ProcessingApp
docker build -t processing-app:latest .
docker save processing-app | (eval $(minikube docker-env) && docker load)

kubectl apply -f rabbitmq_deployment.yaml
kubectl apply -f rabbitmq_service.yaml
kubectl apply -f web_app_deployment.yaml
kubectl apply -f web_app_service.yaml
kubectl apply -f processing_app_deployment.yaml