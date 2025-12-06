# Master node setup
```bash
sudo swapoff -a # Disable swap memory
sudo sysctl -w net.ipv4.ip_forward=1
sudo kubeadm init --apiserver-advertise-address=192.168.50.104 --pod-network-cidr=10.244.0.0/16
# 192.168.50.104 is the device IP address of the master node
```

```
To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/
```
# First pod
<!-- 
```bash
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/tigera-operator.yaml
kubectl create -f [./resources/helpers/custom-resources.yaml](./resources/helpers/custom-resouces.yaml)
``` -->

```bash
kubectl apply -f https://docs.tigera.io/calico/latest/manifests/calico.yaml
```


Calico is a kubernetes networking tool of sorts

# NEED AN INGRESS

## simple ingress?

```kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.0/deploy/static/provider/cloud/deploy.yaml```

## mginx
I'm using nginx because I'm a pleb. I'm not sure if this is the best way to do it, but it works for me.

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```
```bash
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace

# If it gets stuck
# helm upgrade ingress-nginx ingress-nginx/ingress-nginx \
  # --namespace ingress-nginx

#remove
# helm uninstall ingress-nginx --namespace ingress-nginx
# kubectl delete namespace ingress-nginx
# helm rollback ingress-nginx 0 --namespace ingress-nginx

```

Check it

```bash
kubectl get svc --namespace ingress-nginx
```

```bash
kubectl describe svc -n ingress-nginx ingress-nginx-controller
```
get the NodePort - NodePort:                 https  32288/TCP for me
main pod ip 192.168.50.104
# Useful commands

## ```kubeadm reset``` - Cleanup the mess left behind by the failed ```kubeadm init```

## list nodes ```kubectl get nodes```

## display cluster info/ips ```kubectl cluster-info```


## Make control plane a node too

- kubectl taint nodes <node-name> node-role.kubernetes.io/control-plane:NoSchedule-
kubectl taint nodes bosgame-1 node-role.kubernetes.io/control-plane:NoSchedule-
- kubectl taint nodes <node-name> node-role.kubernetes.io/master:NoSchedule-

# Fixes

## no server connection 

```bash
sudo systemctl stop kubelet
sudo systemctl start kubelet
kubectl version
sudo swapoff -a 
sudo systemctl restart kubelet
kubectl version
```

/home/cole/pt_hdd