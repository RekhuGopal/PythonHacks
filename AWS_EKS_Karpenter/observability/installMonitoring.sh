#!/bin/bash
# https://karpenter.sh/docs/getting-started/getting-started-with-eksctl/

helm repo add grafana-charts https://grafana.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

kubectl create namespace monitoring

curl -fsSL https://raw.githubusercontent.com/aws/karpenter/"${KARPENTER_VERSION}"/website/content/en/preview/getting-started/getting-started-with-karpenter/prometheus-values.yaml | tee prometheus-values.yaml

helm install --namespace monitoring prometheus prometheus-community/prometheus --values prometheus-values.yaml


curl -fsSL https://raw.githubusercontent.com/aws/karpenter/"${KARPENTER_VERSION}"/website/content/en/preview/getting-started/getting-started-with-karpenter/grafana-values.yaml | tee grafana-values.yaml

cat << EOF >> grafana-values.yaml
service:
  enabled: true
  type: LoadBalancer
  port: 80
  targetPort: 3000
  annotations: {}
  labels: {}
  portName: service
  appProtocol: ""
EOF
helm install --namespace monitoring grafana grafana-charts/grafana --values grafana-values.yaml
EOS