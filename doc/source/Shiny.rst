Shiny application
=====

In the section, we describes how to create a Shiny application for **SHINY_AWS**

Shiny application basis
------

There are at least **Four** files in the directory where holds the application:

- ``ui.R``: the frontend design
- ``server.R``: the backend server
- ``shiny-server.conf``: Shiny server configuration file
- ``cloud-init.sh``: user data for AWS

``ui.R``, ``server.R`` and ``shiny-server.conf`` are common Shiny files that are needed for any Shiny deployment, while ``cloud-init.sh`` is specific for AWS, which is used to provide additional user inputs when initializing an AWS instance.

An minimum example for ``cloud-init.sh`` is shown below

.. code-block:: bash

   #!/bin/bash
   sudo aws s3 cp s3://xxxx-shiny-app/r/hello_world/ /srv/shiny-server/app/hello_world --recursive
   sudo cp -rf /srv/shiny-server/app/hello_world/shiny-server.conf /etc/shiny-server

The above example does two things: (1) copying the Shiny application from S3 to an AWS instance, and (2) putting the server configuration in the required location


Upload Shiny application to S3
------

All the Shiny application used in **SHINY_AWS** must be uploaded to S3. 

An script ``etc/scripts/copy_shiny.py`` is provided to copy/sync the application. We need to configure the following parameters in the scripts:

.. code-block:: bash

   shiny_app_local = "etc/examples/hello_world"
   shiny_app_s3 = "s3://xxx-shiny-app/r/"

where ``shiny_app_local`` should point to the local Shiny application development (where contains ``ui.R``, ``server.R`` etc.), 
and ``shiny_app_s3`` is the S3 destination where the Shiny application to be sit.