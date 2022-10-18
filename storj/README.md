setup onetime:
https://docs.storj.io/node/dependencies/identity

## secret 2 k8s

`kubectl -n storj create secret generic storj --from-file=./secrets/`

```
Name:         storj
Namespace:    storj
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
identity.key:   241 bytes
ca.cert:        558 bytes
ca.key:         241 bytes
identity.cert:  1096 bytes
```