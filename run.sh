


#run in interactive mode
docker run -e HOSTED_ZONE_ID="Z103409721PN3DZHMI40A" --restart=always --name CompareDNS -it compare_dns

# run in detached mode
#docker run --rm --name test -d helloworld
#docker run --restart=always --name CompareDNS -d compare_dns


