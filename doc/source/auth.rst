.. _shiny_aws_auth:

Authentication
=====

This document provides some notes about how to apply authentication for EC2 hosted Shiny application via `nginx`

Step 1: Install nginx
"""""""""
``nginx`` and ``apache2-utils`` should be installed as:

.. code-block:: bash

    sudo apt-get install nginx
    sudo apt-get install apache2-utils


Step 2: Stop the existing Shiny and Nginx services
"""""""""
If ``nginx`` and ``shiny`` are active, we need to shut them down:

.. code-block:: bash

    sudo service nginx stop
    sudo systemctl stop shiny-server


Step 3: Update Nginx configuration as below
"""""""""
First we need to open the configuration as

.. code-block:: bash

    sudo vi /etc/nginx/sites-available/default

Then we can update/rewrite the configuration as:

.. code-block:: bash

    server {
        listen 80;
        location / {
            proxy_pass http://127.0.0.1:3838/;
            proxy_redirect http://127.0.0.1:3838/ $scheme://$host/;
            # note, the following 3 lines added 2016-07-11, see updates section
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            auth_basic "Username and Password are required";
            auth_basic_user_file /etc/nginx/.htpasswd;
            }
        }


Step 4: Add Nginx into Shiny server configuration
"""""""""
We need to Open the shiny server configuration as:

.. code-block:: bash

    sudo vi /etc/shiny-server/shiny-server.conf


Then we should update the listner IP as:

.. code-block:: bash

    server{
        listen 3838 127.0.0.1;
        location / {
          ....
        }
    }

Step 5: Create the username/password
"""""""""

An interactive way for creating the user `exampleuser`:

.. code-block:: bash

    sudo htpasswd -c /etc/nginx/.htpasswd exampleuser

Or, one line method for creating the user `exampleuser` as:

.. code-block:: bash

    sudo htpasswd -b -c /etc/nginx/.htpasswd exampleuser password

.. note::

    Note that the above commands will overwrite all the existing users if you just want to append a new user: ``htpasswd /etc/nginx/.htpasswd newuser`` (by simply just removing ``-c``)

Step 6: Restart Nginx and Shiny as:
"""""""""
Last we just need to restart ``nginx`` and ``shiny`` as:

.. code-block:: bash
    sudo systemctl start shiny-server
    sudo service nginx start

Last we can access the page at your own elastic IP on AWS

We also can check ``nginx`` status as: ``service nginx status``.

.. note::

    There are some references for ``nginx`` such as `Link1 <https://www.r-bloggers.com/2016/07/shiny-server-on-aws/>`_, and `Link2 <https://www.databentobox.com/2020/05/03/secure-shinyproxy/#step-1-preparing-configuration-files>`_