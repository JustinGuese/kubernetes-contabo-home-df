helm install elk-logstash elastic/logstash -f values.yaml -n elk

helm install elk-filebeat elastic/filebeat -f values-filebeat.yaml -n elk

because of drunk elastic developers `k apply -f fakesecret.yaml `

then dat sheeet shows up in index management as filebeat*
