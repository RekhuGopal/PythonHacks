az login --use-device-code

az aks get-credentials --name "aksdatadogdemo" --resource-group "cloudquicklabs"

helm repo add datadog https://helm.datadoghq.com
helm install datadog-operator datadog/datadog-operator
kubectl create secret generic datadog-secret --from-literal api-key=394470902a015fab37d439e8fcfeb1bb


kubectl apply -f datadog-agent.yaml

