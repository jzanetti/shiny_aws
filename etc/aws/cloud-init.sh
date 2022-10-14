#!/bin/bash

sudo apt-get update
sudo apt install unzip

# install awscli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# create tag
export instance_id=`cat /var/lib/cloud/data/instance-id`
sudo aws ec2 create-tags --resources $instance_id --tag Key=Name,Value='base_image'

# install r-shiny
sudo apt install gdebi-core
sudo apt-get install r-base -y
sudo apt-get install r-base-dev -y
sudo su - -c "R -e \"install.packages('shiny', repos='http://cran.rstudio.com/')\""
wget https://download3.rstudio.org/ubuntu-18.04/x86_64/shiny-server-1.5.18.987-amd64.deb
sudo gdebi -n shiny-server-1.5.18.987-amd64.deb


# install leaflet
sudo apt-get install libgdal-dev -y
sudo R -e 'install.packages(c("leaflet", "sf"))'

# install docker
sudo apt-get update
sudo apt-get install docker.io docker-compose -y

# install authentication
# user: shiny_aws; password: 12345
sudo apt-get install -y nginx
sudo apt-get install -y apache2-utils
sudo aws s3 cp s3://mot-shiny-app/auth/aginx.cfg /etc/nginx/sites-available/default
sudo htpasswd -b -c /etc/nginx/.htpasswd shiny_aws 12345

