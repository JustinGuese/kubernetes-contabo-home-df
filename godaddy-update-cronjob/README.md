Docker / Kubernetes tool to update the IP on godaddy if the router changes IP adresses.

"Open Source" variant for DyDNS, no-ip and others.

Runs a kubernetes job every hour and updates the ip using a kubernetes cronjob

Dockerhub: https://hub.docker.com/repository/docker/guestros/docker-godaddy-dns-updater

# deploy to kubernetes

add your domain/subdomains in the kubernetes/domain-dns-check-cronjob.yaml file and create a secret containing your godaddy api keys (see next step). then apply the cronjob to your cluster with:

`kubectl apply -f kubernetes/domain-dns-check-cronjob.yaml`

## environment variables

for docker just copy paste the `.env-example` and rename it to `.env`

for kubernetes create a secret with:

`kubectl create secret generic godaddy --from-literal=GODADDY_PUBLIC_KEY=2312123123 --from-literal=GODADDY_SECRET=123213123`