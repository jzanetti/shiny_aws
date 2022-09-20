#!/bin/bash

# copy shiny codes
sudo mkdir -p /srv/shiny-server/myapp
sudo aws s3 cp s3://mot-shiny-app/r/hello_world_map /srv/shiny-server/myapp/hello_world_map --recursive
sudo chmod -R 777 /srv/shiny-server/myapp/hello_world_map

# copy inputs:
sudo aws s3 cp s3://mot-shiny-app/etc/tmp/hello_world_map/income.rds /tmp/hello_world_map/income.rds

# start R shiny
sudo cp -rf /srv/shiny-server/myapp/hello_world_map/shiny-server.conf /etc/shiny-server
# sudo systemctl restart shiny-server