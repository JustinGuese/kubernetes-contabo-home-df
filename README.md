# kubernetes-contabo-home-df

IP: 161.97.78.147
https://www.linuxtechi.com/install-kubernetes-on-ubuntu-22-04/

## install

### 1. cert manager

https://cert-manager.io/docs/installation/

```
helm install \
        cert-manager jetstack/cert-manager \
        --namespace cert-manager \
        --create-namespace \
        --set installCRDs=true
kubectl apply -f ingress/df-clusterissuer.yaml

```

### 3. argo ci cd

```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

