

#run in interactive mode
#docker run --rm --net=host --name test -it helloworld

# run in detached mode
#docker run --rm --name test -d helloworld
docker run --restart=always --name CompareDNS -d compare_dns


