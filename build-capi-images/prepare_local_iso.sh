#!/bin/sh

set -ex

PACKER_OS_TARGET=$1

ISO_URL=$(jq -r .iso_url $PACKER_OS_TARGET)
ISO_FILENAME=$(echo ${ISO_URL##*/})
ISO_LOCAL="/home/jenkins/cdimages/${ISO_FILENAME}"

ISO_CHECKSUM_ORIG=$(jq -r .iso_checksum $PACKER_OS_TARGET)
ISO_CHECKSUM_TYPE=$(jq -r .iso_checksum_type $PACKER_OS_TARGET)
ISO_CHECKSUM_EXEC="${ISO_CHECKSUM_TYPE}sum"

if [ ! -f "$ISO_LOCAL" ]; then
        echo "Downloading $ISO_LOCAL"
        curl $ISO_URL --output $ISO_LOCAL
fi

ISO_CHECKSUM_LOCAL=$($ISO_CHECKSUM_EXEC $ISO_LOCAL | awk '{print $1}')
if [ $ISO_CHECKSUM_ORIG != $ISO_CHECKSUM_LOCAL ]; then
        echo "ISO checksum was different. Something wrong!"
        exit 1
fi

ISO_LOCAL=${ISO_LOCAL} envsubst < packer_taco.json > packer_taco_tmp.json
mv packer_taco_tmp.json packer_taco.json
