# kubernetes-contabo-home-df

93.104.55.161
2001:a61:506b:c101:d07f:9f45:c12e:2092




IP: 195.88.87.230
2a02:c206:3009:9907::1
old contabo: 161.97.78.147
IP Homeserver: 93.104.55.161

ssh root@195.88.87.230 -p 223

https://www.linuxtechi.com/install-kubernetes-on-ubuntu-22-04/

# nginx install

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.metrics.enabled=true \
  --set-string controller.podAnnotations."prometheus\.io/scrape"="true" \
  --set-string controller.podAnnotations."prometheus\.io/port"="10254" \
  --set controller.service.type=LoadBalancer \
  --set controller.service.ports.http=80 \
  --set service.annotations."metallb\.universe\.tf/address-pool"=singlenode \
  --set controller.service.ports.https=443 

helm repo add metallb https://metallb.github.io/metallb
helm install metallb metallb/metallb --create-namespace --namespace metallb-system
kubectl apply -f metallb/metallb.yaml

### optional promehtues logging nginx setup

kubectl apply --kustomize github.com/kubernetes/ingress-nginx/deploy/prometheus/

kubectl apply --kustomize github.com/kubernetes/ingress-nginx/deploy/grafana/



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

## install

```
sudo snap install microk8s --classic --channel=latest/stable
microk8s start
microk8s enable dns ingress metrics-server rbac hostpath-storage
microk8s config show
```

edit kubeconfig acccordingly


### 3. argo ci cd

```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 3. sealed secrets

```
helm install sealed-secrets -n kube-system --set-string fullnameOverride=sealed-secrets-controller sealed-secrets/sealed-secrets 
```

kubectl create secret generic secret-name --dry-run=client --from-literal=foo=bar -o [json|yaml] | \
    kubeseal \
      --controller-name=sealed-secrets-controller \
      --controller-namespace=kube-system \
      --format [json|yaml] --cert mycert.pem > mysealedsecret.[json|yaml]

3. Apply the sealed secret

    kubectl create -f mysealedsecret.[json|yaml]

### 4. velero backups

https://github.com/vmware-tanzu/velero-plugin-for-aws

dfcontabo-kubernetes-backups-velero

*velero needs restic for filesystem backup*



`nano cloudcreds`

```
[default]
aws_access_key_id=<AWS_ACCESS_KEY_ID>
aws_secret_access_key=<AWS_SECRET_ACCESS_KEY>
```

**apparently only works with openebs!!**

microk8s enable openebs

kubectl patch storageclass openebs-hostpath -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

kubectl patch storageclass local-path -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'

```

# storj old
velero install \
--use-restic \
--provider aws \
--plugins velero/velero-plugin-for-aws \
--bucket df-k8s-backup \
--secret-file ./cloudcreds \
--backup-location-config region=eu1,s3ForcePathStyle="true",s3Url=https://gateway.storjshare.io


# old backböaze
velero install \
--use-restic \
--provider aws \
--plugins velero/velero-plugin-for-aws \
--bucket dfhome-kubernetes-backups-velero \
--secret-file ./cloudcreds \
--backup-location-config region=eu-central-003,s3ForcePathStyle="true",s3Url=https://s3.eu-central-003.backblazeb2.com,region=eu-central-003 \
--snapshot-location-config region=eu-central-003

# microk8s specific
kubectl -n velero patch daemonset.apps/restic --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/volumes/0/hostPath/path", "value":"/var/snap/microk8s/common/var/lib/kubelet/pods"}]' 
```
  <!-- --snapshot-location-config region=eu-central-1 \ -->


# velero specific
```
kubectl -n velero patch daemonset.apps/restic --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/volumes/0/hostPath/path", "value":"/var/lib/rancher/k3s/agent/kubelet/pods"}]'
```

make annotations for volumes in deployments
annotations:
    backup.velero.io/backup-volumes: mariadb-pv

schedule:

`velero create schedule weekly-backup --schedule="0 2 * * */7" --exclude-namespaces openebs,velero,kube-system`

velero schedule create fullbackup --schedule="1 2 * * */3" # alle 3 tache

for myopiagraph
velero schedule create myopiabackup --schedule="1 2 * * *" --include-namespaces myopia --ttl 360h

To show all stored backups list (name, status, creation and expiration date)
$ velero get backups

restore

**restore is nondestructive, meaning you need to delete the PV before**

velero restore create --from-backup backup_name

# To show one specific backup details
$ velero describe backup backup_name


# observability

(user/pass: admin/prom-operator)

### (disabled for now) NFS setup

https://microk8s.io/docs/nfs

/srv/nfs

```
sudo apt-get install nfs-kernel-server
sudo mkdir -p /srv/nfs
sudo chown nobody:nogroup /srv/nfs
sudo chmod 0777 /srv/nfs
# export setup
sudo mv /etc/exports /etc/exports.bak
echo '/srv/nfs/* 192.168.178.0/24(rw,sync,no_subtree_check,no_root_squash)' | sudo tee /etc/exports
sudo systemctl restart nfs-kernel-server
# host
helm repo add csi-driver-nfs https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/charts
helm install csi-driver-nfs csi-driver-nfs/csi-driver-nfs \
    --namespace kube-system \
    --set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet
kubectl apply -f nfs-csi/nfs-storageclass.yaml
# switching from an old storageclass to a new one during restore
kubectl apply -f nfs-csi/velero-switch-storage-class.yaml
```

# hardening the server

## ufw

```
sudo ufw default allow outgoing
sudo ufw default deny incoming
# ssh, https
sudo ufw allow http
sudo ufw allow https
sudo ufw allow 223 # ssh
# microk8s
sudo ufw allow 16443
sudo ufw allow 10250
sudo ufw allow 10255
sudo ufw allow 25000
sudo ufw allow 12379
sudo ufw allow 10257
sudo ufw allow 10259
sudo ufw allow 19001
sudo ufw allow 4789/udp

sudo ufw enable
```

# high availability split

curl -sfL https://get.k3s.io | K3S_TOKEN=SECRET sh -s - server --cluster-init
curl -sfL https://get.k3s.io | K3S_TOKEN=SECRET sh -s - server --server https://datafortress.duckdns.org:6443




---

old microk8s:

datafortress.duckdns.org

:25000/218fcc207c307b431cc20943496be18e/da92c056aab7

microk8s join datafortress.duckdns.org:25000/218fcc207c307b431cc20943496be18e/da92c056aab7

need to set hostname in local dfhome to remote ip
nano /etc/hosts 
116.203.28.167 dfcloudk8s