#!/bin/bash
sudo aws s3 cp s3://mot-shiny-app/r/hello_world/ /srv/shiny-server/app/hello_world --recursive
sudo cp -rf /srv/shiny-server/app/hello_world/shiny-server.conf /etc/shiny-server
# sudo systemctl restart shiny-server