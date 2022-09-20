#!/bin/bash

# ----------------------
# get the shiny image
# ----------------------
aws ecr get-login-password --region ap-southeast-2 | sudo docker login --username AWS --password-stdin 839525146093.dkr.ecr.ap-southeast-2.amazonaws.com
sudo docker pull 839525146093.dkr.ecr.ap-southeast-2.amazonaws.com/shiny:hello_world_map

# ----------------------
# start docker based shiny server
# ----------------------
sudo docker run --rm -p 8787:8787 839525146093.dkr.ecr.ap-southeast-2.amazonaws.com/shiny:hello_world_map >& log &