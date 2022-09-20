FROM rocker/shiny:latest

USER root

# install R packages required
RUN R -e 'install.packages(c(\
              "shiny", \
              "leaflet", \
              "sf" \
            ) \
        )'

# install aws
RUN sudo apt-get update \
    && sudo apt-get install curl \ 
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \ 
    && unzip awscliv2.zip \
    && sudo ./aws/install

# copy the app directory into the image
RUN mkdir /srv/shiny-server/myapp
COPY r/hello_world_map/*.R /srv/shiny-server/myapp/hello_world_map/

# copy the crash data script
RUN mkdir /tmp/hello_world_map
COPY r/hello_world_map/etc/income.rds /tmp/hello_world_map/income.rds

# by default the port is 3838, here we change it to 8787
COPY r/hello_world_map/shiny-server.conf /etc/shiny-server/shiny-server.conf

# run app
CMD ["/usr/bin/shiny-server"]