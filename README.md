# GPU_k8s

## Set up env in proxmox 

skip this if you are using bare machine.

Ref : https://www.youtube.com/watch?v=U1VzcjCB_sY&t=452s 
### Options page:

`Start at boot : Yes`

`Start/Shutdown order : add start up delay 15 sec` (Only on worker nodes.)

`QEMU Guest Agent : Enable`

Run this command in both controller and worker nodes.

```
sudo apt install qemu-guest-agent
```

## Preapare before set up cluster
Run this command in both controller and worker nodes.

```
sudo apt update && sudo apt dist-upgrade
```

### Set up static IP
```
cd /etc/netplan
```

Backup file before modify
```
sudo cp 50-cloud-init.yaml 50-cloud-init.yaml.bak
```
```
sudo vi 50-cloud-init.yaml 
```
Edit file
```
network:
    version: 2
    ethernets:
        eth0:
            addresses: [10.10.10.213/24]
            nameservers:
                addresses: [10.10.10.1]
            routes:
                - to: default
                  via: 10.10.10.11
```
```
sudo netplan try
```
Check hostname & Information
```
cat /etc/hostname
cat /etc/hosts
```

## Install container runtime
Run these command in both controller and worker nodes.
```
sudo apt install containerd
```
Check containerd status
```
systemctl status containerd
```
Create directory
```
sudo mkdir /etc/containerd
```
Place default configuration
```
containerd config default | sudo tee /etc/containerd/config.toml
```
```
sudo vi /etc/containerd/config.toml
```
Find keyword `runc.options` and make `SystemdCgroup = true`.

## Disable swap
Run this command in both controller and worker nodes.

Check swap
```
free -m
```
```
sudo vi /etc/fstab
```
If it have any `swap` you can comment by using `#` like `#UUID=xxx-xxx-xxx-xxx none swap sw 0 0`

Turn off all swap processes
```
sudo swapoff -a
```
Reboot the system
```
sudo reboot
```
After rebooting, you can confirm that swap is disabled by running
```
swapon --show
```
## Enable bridging
Run this command in both controller and worker nodes.

```
sudo vi /etc/sysctl.conf
```
Find line `#net.ipv4.ip_forward=1` and uncomment it like this `net.ipv4.ip_forward=1`.

## Enable br_netfilter
Run this command in both controller and worker nodes.

```
sudo vi /etc/modules-load.d/k8s.conf
```
Add content.
```
br_netfilter
```
## After finish all process reboot all machines
```
sudo reboot
```
## Install Kubernetes
Ref : https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/

Run these command in both controller and worker nodes.

1.Update the `apt` package index and install packages needed to use the Kubernetes `apt` repository:
```
sudo apt-get update
```
- apt-transport-https may be a dummy package; if so, you can skip that package
```
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
```

2.Download the public signing key for the Kubernetes package repositories. The same signing key is used for all repositories so you can disregard the version in the URL:

- If the directory `/etc/apt/keyrings` does not exist, it should be created before the curl command, read the note below.
```
 sudo mkdir -p -m 755 /etc/apt/keyrings
```
```
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
```
3.Add the appropriate Kubernetes `apt` repository. Please note that this repository have packages only for Kubernetes 1.31; for other Kubernetes minor versions, you need to change the Kubernetes minor version in the URL to match your desired minor version (you should also check that you are reading the documentation for the version of Kubernetes that you plan to install).

- This overwrites any existing configuration in `/etc/apt/sources.list.d/kubernetes.list`
```
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

4.Update the `apt` package index, install kubelet, kubeadm and kubectl, and pin their version:
```
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```
## Only using proxmox : Build worker node template
Only worker node.
```
sudo cloud-init clean
sudo rm -rf /var/lib/cloud/instances
sudo truncate -s 0 / etc/machine-id
sudo rm /var/lib/dbus/machine-id
sudo ln -s /etc/machine-id /var/lib/dbus/machine-id
ls -l /var/lib/dbus/machine-id
cat /etc/machine-id
sudo poweroff
```
Then create template using this node and clone node by using this template.

## Run `kubeadm init` command
Only controller node.

```
sudo kubeadm init --control-plane-endpoint=[IP-ADDRESS CTRLR NODE] --node-name [HOSTNAME CTRLR NODE] --pod-network-cidr=10.244.0.0/16
```
Example: 
```
sudo kubeadm init --control-plane-endpoint=10.10.10.213 --node-name k8s-ctrlr --pod-network-cidr=10.244.0.0/16
```

We will get the join-command like this :
```
kubeadm join 10.10.10.213:6443 --token to45gs.80prk3u3zwh6033 \
--discovery-token-ca-cert-hash sha256:5f20c66766ff844dc8466ae4a687846aeb6975321278528a095d0e4c88dee06 \
-- control-plane
```
Coppy this command and keep in .txt file

Run these command to allow local user access the cluster.
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Check that everything is work.
```
kubectl get pods --all-namespaces
```

## Adding an overlay network to cluster
Ref : https://docs.tigera.io/calico/latest/getting-started/kubernetes/quickstart

1.Install the Tigera Calico operator and custom resource definitions.
```
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.1/manifests/tigera-operator.yaml
```
2.Install Calico by creating the necessary custom resource.
```
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.1/manifests/custom-resources.yaml
```
3.Confirm that all of the pods are running with the following command.
```
watch kubectl get pods -n calico-system
```

## Join worker nodes to cluster
Only worker nodes.

Run join-command with `sudo`
```
sudo kubeadm join 10.10.10.213:6443 --token to45gs.80prk3u3zwh6033 \
--discovery-token-ca-cert-hash sha256:5f20c66766ff844dc8466ae4a687846aeb6975321278528a095d0e4c88dee06 \
-- control-plane
```

If join-command already expire we can use `kubeadm token create --print-join-command` in controller node to print join-command again.

Check that everything is work.
```
kubectl get nodes
```

