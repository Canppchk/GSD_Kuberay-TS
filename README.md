# GPU_k8s

## Set up env in proxmox 
skip this if you are using bare machine.

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
If it have any `swap` you can comment by using `#`

