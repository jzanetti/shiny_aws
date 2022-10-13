#!/bin/bash
sudo aws s3 cp s3://mot-shiny-app/r/hello_world/ /srv/shiny-server/app/hello_world --recursive
sudo cp -rf /srv/shiny-server/app/hello_world/shiny-server.conf /etc/shiny-server

# sudo aws s3 cp s3://mot-shiny-app/r/asg_test/add-ip.sh /tmp/add-ip.sh
# sudo chmod -R 777 /tmp/add-ip.sh
# sudo crontab -l > /tmp/mycrontab
# echo "* * * * * /tmp/add-ip.sh" >> /tmp/mycrontab
# sudo crontab -u ubuntu /tmp/mycrontab

sudo service nginx stop
sudo systemctl restart shiny-server