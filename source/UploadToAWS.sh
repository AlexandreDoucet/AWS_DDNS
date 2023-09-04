

RPI_EXT_IP=$(curl http://ifconfig.co)

rm -f -- r52-update.json
touch r53-update.json

cat > r53-update.json << __EOF__
  {
    "Changes": [
      {
        "Action": "UPSERT",
        "ResourceRecordSet": {
          "Name": "home.techtinkerhub.com",
          "Type": "A",
          "TTL": 600,
          "ResourceRecords": [
            {
              "Value": "${RPI_EXT_IP}"
            }
          ]
        }
      }
    ]
  }
__EOF__


aws route53 change-resource-record-sets --hosted-zone-id Z103409721PN3DZHMI40A --change-batch file://r53-update.json 


rm -f -- /tmp/r52-update.json
