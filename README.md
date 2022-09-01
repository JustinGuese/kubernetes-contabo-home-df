# kubernetes-contabo-home-df

IP: 161.97.78.147


## install

### 1. nginx ingress

https://kubernetes.github.io/ingress-nginx/deploy/#quick-start

```
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```

### 2. cert manager

https://cert-manager.io/docs/installation/

```
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.9.1/cert-manager.yaml
kubectl apply -f ingress/df-clusterissuer.yaml

```

### 3. argo ci cd

```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

