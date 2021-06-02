#!/bin/bash

set -x

for img in $(ls sonobuoy_imgs/)
do
        sudo docker image load -i sonobuoy_imgs/$img
done
