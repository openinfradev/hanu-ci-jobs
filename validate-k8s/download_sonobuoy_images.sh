#!/bin/bash

ALL_IMGS=""

mkdir sonobuoy_imgs

for img in $(sudo KUBECONFIG=target_kubeconfig ./sonobuoy images)
do
        ALL_IMGS+=" $img"
        sudo docker image save $img > sonobuoy_imgs/${img##*/}.tar
done

# Remove failed images with size 0
cd sonobuoy_imgs && ls -lh | awk '{ if ($5 == "0") print $9}' | xargs rm
