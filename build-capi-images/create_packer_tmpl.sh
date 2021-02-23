#!/bin/sh

set -ex

if [ -z "$1" ]
then
    K8S_VERSION="1.20.2"
else
    K8S_VERSION=$1
fi

K8S_SERIES=$(echo ${K8S_VERSION} | awk -F'.' '{print $1"."$2}')

cat << EOF > ./packer_taco.json
{
  "kubernetes_series": "v${K8S_SERIES}",
  "kubernetes_semver": "v${K8S_VERSION}",
  "kubernetes_deb_version": "${K8S_VERSION}-00",
  "disk_size": "5240",
  "format": "raw",
  "iso_url": "\$ISO_LOCAL"
}
EOF
