#!/bin/bash
helm install wordpress-leave bitnami/wordpress \
    --set wordpressUsername=admin \
    --set wordpressPassword="sssiiikret" \
    --set wordpressEmail=info@datafortress.cloud \
    --set wordpressBlogName="Leave Shop" \
    --set service.type=ClusterIP \
    --set persistence.size=2Gi \
    --set autoscaling.enabled=true \
    --set autoscaling.targetCPU=80 \
    --set autoscaling.targetMemory=80 \
    --set mariadb.primary.persistence.size=500Mi \
    -n wordpress-leave