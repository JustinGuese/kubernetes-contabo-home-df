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

`nano cloudcreds`

```
[default]
aws_access_key_id=<AWS_ACCESS_KEY_ID>
aws_secret_access_key=<AWS_SECRET_ACCESS_KEY>
```

```
velero install \
  --provider velero.io/aws \
  --bucket dfcontabo-kubernetes-backups-velero \
  --plugins velero/velero-plugin-for-aws:v1.4.0 \
  --backup-location-config region=eu-central-1 \
  --snapshot-location-config region=eu-central-1 \
  --secret-file ./cloudcreds
```

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