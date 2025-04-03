# Kuberay Workloads

## Install Kuberay

Install Kuberay-operator
```
helm install kuberay-operator kuberay/kuberay-operator --version 1.1.1
```

Install ray cluster
```
helm install raycluster1 kuberay/ray-cluster --version 1.1.1 -f values-cluster.yaml
helm install raycluster2 kuberay/ray-cluster --version 1.1.1 -f values-cluster.yaml
helm install raycluster3 kuberay/ray-cluster --version 1.1.1 -f values-cluster.yaml
```


