

RPI_EXT_IP=$(curl http://ifconfig.co)

rm -f -- r52-update.json
touch r53-update.json

cat > r53-update.json << __EOF__
  {
    "Changes": [
      {
        "Action": "UPSERT",
        "ResourceRecordSet": {
          "Name": "${DOMAIN}",
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


aws route53 change-resource-record-sets --hosted-zone-id $HOSTED_ZONE_ID --change-batch file://r53-update.json --profile $AWS_PROFILE_NAME


rm -f -- /tmp/r52-update.json
