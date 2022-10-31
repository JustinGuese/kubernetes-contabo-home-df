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


Dont forget to enable ufw portforward etc 31008, 28967

## simple docker run

docker run -d --restart unless-stopped --stop-timeout 300 \
    -p 28967:28967/tcp \
    -p 28967:28967/udp \
    -p 14002:14002 \
    -e WALLET="0x00cb28C0dd07f9277C724E525f895f45b42B6ad7" \
    -e EMAIL="guese.justin@gmail.com" \
    -e ADDRESS="datafortress.duckdns.org:28967" \
    -e STORAGE="2TB" \
    --user $(id -u):$(id -g) \
    --mount type=bind,source="/home/df/.local/share/storj/identity/storagenode",destination=/app/identity \
    --mount type=bind,source="/mnt/hdd/storj/",destination=/app/config \
    --name storagenode storjlabs/storagenode:latest

### paris server


docker run --rm -e SETUP="true" \
    --user $(id -u):$(id -g) \
    --mount type=bind,source="/home/dfserver/.local/share/storj/identity/storagenode",destination=/app/identity \
    --mount type=bind,source="/home/dfserver/storj",destination=/app/config \
    --name storagenodesetup storjlabs/storagenode:latest

docker run -d --restart always --stop-timeout 300 \
    -p 28967:28967/tcp \
    -p 28967:28967/udp \
    -p 127.0.0.1:14002:14002 \
    -e WALLET="0x00cb28C0dd07f9277C724E525f895f45b42B6ad7" \
    -e EMAIL="guestros@gmx.de" \
    -e ADDRESS="163.172.50.108:28967" \
    -e STORAGE="0.9TB" \
    --user $(id -u):$(id -g) \
    --mount type=bind,source="/home/dfserver/.local/share/storj/identity/storagenode",destination=/app/identity \
    --mount type=bind,source="/home/dfserver/storj",destination=/app/config \
    --name storagenode storjlabs/storagenode:latest