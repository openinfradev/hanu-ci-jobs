#! /bin/bash

result_file=$(sonobuoy retrieve)
sonobuoy results $result_file
sonobuoy results --mode detailed $result_file |  jq '. | select(.status == "failed") | .details'
