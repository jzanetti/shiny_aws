FROM rocker/shiny:latest

USER root

# install R packages required 
RUN R -e 'install.packages(c(\
              "shiny", \
              "shinydashboard" \
            ) \
          )'


# copy the app directory into the image
RUN mkdir /srv/shiny-server/app
COPY *.R /srv/shiny-server/app/

# COPY shiny-server.conf /etc/shiny-server/shiny-server.conf

# by default the port is 3838, here we change it to 8787
#RUN sed -i -e 's/\blisten 3838\b/listen 8788/g' /etc/shiny-server/shiny-server.conf
#RUN sed -i -e 's/\blocation/\b/location/g' /etc/shiny-server/shiny-server.conf
COPY shiny-server.conf /etc/shiny-server/shiny-server.conf


# run app
CMD ["/usr/bin/shiny-server"]