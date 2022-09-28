# kubernetes-contabo-home-df

IP: 195.88.87.230
161.97.78.147
IP Homeserver: 93.104.55.161


https://www.linuxtechi.com/install-kubernetes-on-ubuntu-22-04/

## install

```
sudo snap install microk8s --classic --channel=latest/stable
microk8s start
microk8s enable dns ingress metrics-server rbac
microk8s config show
```

edit kubeconfig acccordingly

### NFS setup

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

```
velero install \
  --provider velero.io/aws \
  --bucket dfhome-kubernetes-backups-velero \
  --plugins velero/velero-plugin-for-aws:v1.4.0 \
  --backup-location-config region=eu-central-1 \
  --use-volume-snapshots=false \
  --use-restic \
  --backup-location-config \
      s3Url=https://s3.eu-central-003.backblazeb2.com,region=eu-central-003 \
  --secret-file ./cloudcreds
```
  <!-- --snapshot-location-config region=eu-central-1 \ -->

make annotations for volumes in deployments
annotations:
    backup.velero.io/backup-volumes: mariadb-pv

schedule:

`velero create schedule bidaily-wordpress-backup --schedule="0 2 * * */2" --include-namespaces wordpressdb,wordpress-easycloudhost,wordpress-bildblatt,wordpress-aipaints`

To show all stored backups list (name, status, creation and expiration date)
$ velero get backups

restore
velero restore create --from-backup backup_name

# To show one specific backup details
$ velero describe backup backup_name


# observability

(user/pass: admin/prom-operator)