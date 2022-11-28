HTTPS
=====

By default, **SHINY_AWS** will provide a link with ``http``, however, for accessing the link securely, ``https`` is usually recommendded.

``Https`` is a protocol that encrypts your communication with a web server. Https can be useful for two things:

  - So nobody can read the communication between you and the web server
  - So you can be sure that you are really really talking to the desired web server, and not to a fake (a so-called man-in-the-middle)

There are two ways to produce a link with ``https``

Inside server
------
When a shiny server is set up, by default a ``http`` link is given. In order to **upgrade** it to a ``https``, 

- We need to configure the server security group. For example, usually in the ``inbound rules`` we have ``HTTP``:

  .. code-block:: bash

    IPv4	HTTP	TCP	80	0.0.0.0/0

  We would need to delete this line, and add a new rule with ``https``, e.g.,

  .. code-block:: bash

    IPv4	HTTPS	TCP	443	0.0.0.0/0

- We should create an open SSL certificate as:

  .. code-block:: bash

    sudo -i
    openssl genrsa -out /etc/ssl/private/apache.key 2048
    openssl req -new -x509 -key /etc/ssl/private/apache.key -days 365 -sha256 -out /etc/ssl/certs/apache.crt

  This will ask you a few questions. The only crucial part is the Common Name. Here you need to enter the **public DNS name** or **the public IP** of your AWS instance.

- Then, let's install Apache2 as:

  .. code-block:: bash

    apt-get install apache2

  Then it should be configured as:

  .. code-block:: bash

    a2enmod

  This will open a dialog that asks you which modules you would like to install. Type the following:

  .. code-block:: bash

    ssl proxy proxy_ajp proxy_http rewrite deflate headers proxy_balancer proxy_connect proxy_html

- We need configure ``/etc/apache2/sites-enabled/000-default.conf`` as:

  .. code-block:: bash

    <VirtualHost *:*>
        SSLEngine on
        SSLCertificateFile /etc/ssl/certs/apache.crt
        SSLCertificateKeyFile /etc/ssl/private/apache.key
        ProxyPreserveHost On
        ProxyPass / http://0.0.0.0:3838/
        ProxyPassReverse / http://0.0.0.0:3838/
        ServerName localhost
    </VirtualHost>

  where ``3838`` is the shiny server IP (e.g., defined in `/etc/shiny-server/shiny-server.conf`). Note that we should not have port ``80`` for the shiny server. 

- Finally we can start ``aparch2`` as:

  .. code-block:: bash
    
    service apache2 restart

.. note::

    Sometime we may get the error ``AH00072: make_sock: could not bind to address [::]:80``. 
    In that case, we can find which program is using ``80`` with ``sudo lsof -i:80``


