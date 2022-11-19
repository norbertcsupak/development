#!/bin/bash

# after running this script , have to  run the garbage cleanup in container > /bin/registry garbage-collect /etc/docker/registry/config.yml
# exit when any command fails
set -e

registry='192.168.4.182:5000'

# concants all images listed in json file into single line string seperated with blank
#images="alpine"
echo "Image:"
read images
echo "Registry User:"
read user
echo "Registry Password:"
read -s password

for image in $images; do
    echo "DELETING: " $image

    # get tag list of image, with fallback to empty array when value is null
    tags=$(curl --user $user:$password -X GET "http://${registry}/v2/${image}/tags/list" | jq -r '.tags // [] | .[]' | tr '\n' ' ')

    echo "A tag: $tags"

    # check for empty tag list, e.g. when already cleaned up
    if [[ -n $tags ]]
    then
        for tag in $tags; do
	    step1=$(curl --user $user:$password -X GET -I -H "Accept: application/vnd.docker.distribution.manifest.v2+json" "http://${registry}/v2/${image}/manifests/${tag}" | awk '$1 == "Docker-Content-Digest:" { print $2 }' | tr -d $'\r') 
	    echo "Step1: ${step1}"
	    curl --user $user:$password -X DELETE "http://${registry}/v2/${image}/manifests/${step1}"
        done

        echo "DONE:" $image
    else
        echo "SKIP:" $image
    fi
done

