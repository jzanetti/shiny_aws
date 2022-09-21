Base AMI
=============

We can create a base AMI to include all the necessary dependancies. An simple script ``etc/scripts/create_base.py`` is provided to create the base image.

.. note::

    We always can run **SHINY_AWS** using the AWS base Linux image. In this case we need to install dependancies ``cloud-init.sh`` at the application, which may result in a slow initiation of an EC2 instance.


Configuration
***********
There are two configurations which we may need to adjust:
- ``cloud-init.sh``: here we need to define the dependancies to be installed, and server authentication if needed
- ``spot_spec.json``: the instance configuration (e.g., the instance type etc.)

An example of ``cloud-init.sh`` is shown below:

.. code-block:: bash
    #!/bin/bash

    sudo apt-get update
    sudo apt install gdebi-core
    sudo apt-get install r-base -y
    sudo apt-get install r-base-dev -y
    sudo su - -c "R -e \"install.packages('shiny', repos='http://cran.rstudio.com/')\""
    wget https://download3.rstudio.org/ubuntu-18.04/x86_64/shiny-server-1.5.18.987-amd64.deb
    sudo gdebi -n shiny-server-1.5.18.987-amd64.deb

    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install

    # install all required R libraries
    sudo R -e 'install.packages(c("tidyr", "DT", "ggplot2", "reshape2", "lubridate", "markdown"))'

    # install docker
    sudo apt-get update
    sudo apt-get install docker.io docker-compose -y

    # install authentication
    # user: shiny_aws; password: 12345
    sudo apt-get install -y nginx
    sudo apt-get install -y apache2-utils
    sudo aws s3 cp s3://mot-shiny-app/auth/aginx.cfg /etc/nginx/sites-available/default
    sudo htpasswd -b -c /etc/nginx/.htpasswd shiny_aws 12345

In the above example, we installed `awscli` and a few R dependancies such as ``tidyr``. A docker server is also installed. 
Besides, we use ``nginx`` to configure the username and password at the end of configuration (in this case, the username is ``shiny_aws`` and password is ``12345``).

Deployment
***********
Deploying the instance with the base image is very simple, we just need to run:

.. code-block:: bash

    python create_base.py

In addition to the locations of configurations, we also need to specify how much we are willing to pay for the spot instance.