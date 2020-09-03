## Creating Kubernetes cluster on physical host from ansible playbook: 

Usage: 

1. set up  variables in /var 
The host IP is :10.0.0.200
Put your host pub key in : roles/create_vms/templates/user-data.j2 - file  

2. create cluster and make inventory of  VM's ip  : 
```
ansible-playbook -i production site.yml  --tags create,inv
```

after creation: 
- the VMs IPs stored in : invetory_file
- accessing master node from host :  ssh -i /home/user/id_rsa ubuntu@master_vm_ip

3. only create inventory :
```
ansible-playbook -i production site.yml  --tags inv
```

4. create VMs + kube cluster : 
```
ansible-playbook -i production site.yml  --tags create,inv,kube
```

5. delete cluster:
```
ansible-playbook -i production site.yml  --tags delete
```
6. Installing Kube cluster  from host with  wrapper.sh [4]  : https://www.digitalocean.com/community/tutorials/how-to-create-a-kubernetes-cluster-using-kubeadm-on-ubuntu-18-04
