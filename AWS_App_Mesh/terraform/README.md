# AWS_EKS_App_Mesh

## Helm Commands
helm repo add eks https://aws.github.io/eks-charts
helm repo update

## Check the service accessibility locally
kubectl exec -it client-svc -c ubuntu -n client-svc -- sh
curl server-svc.server-svc.svc.cluster.local:8080/version

## Check the service accessibility
curl --header "Host: server-svc.devopsbyexample.com" a4848cd5ea6ea40c1ac68f0d05115f34-8a0ac03c1881aada.elb.us-west-2.amazonaws.com 

## Windows 
Invoke-WebRequest -Uri "http://a4848cd5ea6ea40c1ac68f0d05115f34-8a0ac03c1881aada.elb.us-west-2.amazonaws.com/version" -Headers @{"Host"="server-svc.devopsbyexample.com"}


