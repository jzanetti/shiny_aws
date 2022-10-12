Shiny application
=====

In the section, we describe how to create a Shiny application for **SHINY_AWS**

Shiny applications hierarchy
------

**SHINY_AWS** uses a single server to host multiple shiny applications. All shiny applications must sit in one repository (either in _github_ or _gitlab_). For example:

.. code-block:: bash

   - <repository name>
      - shiny-server.conf
      - <shiny app 1>
      - <shiny app 2>
      - ....
      - <shiny app N>

where ``<shiny app ..>`` is a directory contains all the necessary setups for an individual shiny application. ``shiny-server.conf`` is the shiny server configuration file.

An example for the shiny application repository can be accessed `here <https://github.com/jzanetti/shiny_aws_examples>`_.

Shiny application basis
------

As above, ``<shiny app ..>`` is a directory contains an independant shiny application. Within the directory, there are at least **THREE** files:

- ``ui.R``: the frontend design
- ``server.R``: the backend server
- ``cloud-init.sh``: user data for AWS

``ui.R`` and ``server.R`` are common Shiny files that are needed for any Shiny deployment, while ``cloud-init.sh`` is specific for AWS, which is used to provide additional user inputs for initializing an AWS instance.

An minimum example for ``cloud-init.sh`` is shown below

.. code-block:: bash

   sudo aws s3 cp s3://xxxx-shiny-app/r/hello_world/ /srv/shiny-server/app/hello_world --recursive
   sudo cp -rf /srv/shiny-server/app/hello_world/shiny-server.conf /etc/shiny-server

The above example does two things: (1) copying the Shiny application from S3 to an AWS instance, and (2) putting the server configuration in the required location.

During the shiny server deployment, ``<shiny app ..>`` will be checked out through ``git clone`` so it can be picked up by the server in an AWS EC2 instance.