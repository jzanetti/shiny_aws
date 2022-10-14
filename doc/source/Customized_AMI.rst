Customized AMI
=============

We can create a customized AMI to include all the necessary dependancies.

.. note::

    We always can run **SHINY_AWS** using the AWS base Linux image. In this case we need to (re)install dependancies from ``cloud-init.sh`` every time when we bring up an instance.


Configuration
***********
There are two configurations (for ``create_base.py``) which we may need to adapt:

- ``cloud-init.sh``: here we need to define the dependancies to be installed, and server authentication if needed
- ``spot_spec.json``: the instance configuration (e.g., the instance type etc.)

An example of ``cloud-init.sh`` is shown below:

.. code-block:: bash

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

    sudo apt install gdebi-core
    sudo apt-get install r-base -y
    sudo apt-get install r-base-dev -y
    sudo su - -c "R -e \"install.packages('shiny', repos='http://cran.rstudio.com/')\""
    wget https://download3.rstudio.org/ubuntu-18.04/x86_64/shiny-server-1.5.18.987-amd64.deb
    sudo gdebi -n shiny-server-1.5.18.987-amd64.deb

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

In the above example, we installed ``awscli`` and a few R dependancies such as ``tidyr``. A docker server is also installed. 
Besides, we use ``nginx`` to configure the username and password at the end of configuration (in this case, the username is ``shiny_aws`` and password is ``12345``).

Making a customized AMI
***********
Deploying the instance with the base image is very simple, we just need to run:

.. code-block:: bash

    make_base --cloud_init <CLOUD_INIT> 
              --spot_spec <SPOT_SPEC> 
              --ami_name <AMI_NAME> 
              --expected_duration <EXPECTED_DURATION> 
              [--overwrite_ami]

where ``<CLOUD_INIT>`` is the cloud init file, and ``<SPOT_SPEC> `` describes the instance spot. ``<AMI_NAME>`` is the AMI name to be applied. 
``<EXPECTED_DURATION>`` is the expected time that we need to make the AMI, and ``--overwrite_ami`` will overwrite the AMI if it exists.

One example for creating the base image is:

.. code-block:: bash

    make_base --cloud_init etc/aws/cloud-init.sh --spot_spec etc/aws/spot_spec.json --ami_name ami_test_v2.0 --expected_duration 3 --overwrite_ami