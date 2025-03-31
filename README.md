# Kuberay Workloads

## Install nvidia-device plugin

Install gpu-operator without device plugin
```
helm install -n gpu-operator   --generate-name   --create-namespace   --set devicePlugin.enabled=false   --set gfd.enabled=false    nvidia/gpu-operator
```

Install device plugin with mps
```
helm upgrade -i nvdp nvdp/nvidia-device-plugin     --version=0.16.0     --namespace nvidia-device-plugin     --create-namespace     --set gfd.enabled=true     --set config.default=mps2     --set-file config.map.mps2=dp-mps-2.yaml
```
```
helm upgrade -i nvdp nvdp/nvidia-device-plugin \     
		--version=0.16.0 \ 
		--namespace nvidia-device-plugin \    
		--create-namespace \    
		--set gfd.enabled=true \   
		--set config.default=mps10 \    
		--set-file config.map.mps10=dp-mps-10.yaml
```


