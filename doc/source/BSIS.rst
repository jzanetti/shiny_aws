BSIS
=====

This page describes how to deploy a **BSIS** infrastructure

Configuration
------
First we need to create an configuration (the easiest way is to create your own configuration by adapting an existing one)

For **BSIS**, there are two main sections in the configuration

  - **shiny**: the R-Shiny specific setups
  - **user**: user sepecfic information
  - **aws**: AWS specific setups

Configuration (Shiny):
^^^^^^^^^^^
For **shiny**, we need to define where the Shiny application comes from. How to create a Shiny on S3 can be obtained `here <https://shiny-aws-doc.readthedocs.io/en/latest/Shiny.html>`_.

An simple example is given below:

.. code-block:: bash

   shiny: 
      names: 
         hello_world: hello_world/link1
      url: https://github.com/jzanetti/shiny_aws_examples.git
      branch: main
      cred: null

The above provides some basic shiny information: 
   - the Shiny server takes the ``main`` branch from ``https://github.com/jzanetti/shiny_aws_examples.git``. 
   - ``hello_world`` is the only application we want to host, and it will use the link name ``hello_world/link1`` (e.g., the IP for this app will be ``<IP Address>/hello_world/link1``)
   - there is no credentials needed

For private repository we can apply a private token to access the repository. For example, we can have the credentials to access the repository as below:

.. code-block:: bash

   shiny: 
      names: 
         hello_world: hello_world/link1
      url: https://github.com/jzanetti/shiny_aws_examples.git
      branch: main
      cred:     
         user: <user-name>
         token: <token>

Configuration (AWS):
^^^^^^^^^^^

For **aws**, we need to provide usual AWS configurations such as ``VPC``, ``subnets`` and the ``ami`` to be used. An example is given below:

.. code-block:: bash

      aws:
         ImageId: ami-xxxxxxxxxxxxxxx
         KeyName: xxxxxxxxx-key
         SecurityGroupIds:
            - sg-xxxxxxxxx
         SubnetId: subnet-xxxxxxxxx
         InstanceType: t2.medium
         Placement:
            AvailabilityZone: ap-southeast-2a
         IamInstanceProfile:
            Arn: arn:aws:iam::xxxxxxxxx:instance-profile/ShinyApp_role
         BlockDeviceMappings:
            DeviceName: /dev/sda1
            Ebs:
               VolumeType: gp2
               DeleteOnTermination: true
               VolumeSize: 15

Configuration (user):
^^^^^^^^^^^

We will have to provide a few **user** defined parameters:

.. code-block:: bash

      user:
         elastic_ip: eipalloc-xxxxxxxxx
         authentication: true
         spot_price: 0.1

Where:

- ``elastic_ip``: this can be set to ``null`` if we don't want to use AWS Elastic IP.
- ``authentication``: we can set up authentication (using `Nginx <https://www.nginx.com/>`_) for our server (setup for ``nginx`` can be found :ref:`shiny_aws_auth`.).
- ``spot_price``: Spot price we are willing to pay in the EC2 spot market.

An full example for the **BSIS** configuration can be found at ``etc/cfg/bsis.yml``

Deployment
------
The **BSIS** can be deployed under the environment ``shiny_aws``:

.. code-block:: bash

   conda activate shiny_aws
   start_bsis --cfg /tmp/bsis.yml --workdir /tmp --lifespan 60

Where ``--cfg`` is the configuration for **BSIS** and ``--workdir`` is the working directory holds all the intermediate files. 
``lifespan`` indicates how long the instance will be active (in minutes). By default, ``lifespan`` is 60 minutes, while 
in production we can set it to `unlimited` (e.g., being defined by `UNLIMITED_LIFESPAN_FLAG`). Please set ``lifespan`` 
carefully since AWS charges us every seconds we use the server.

After the deployment, we should be able to find an EC2 instance in the console with the shiny application being installed.


Using HTTPS
------
By default, **BSIS** in ***SHINY_AWS** will provide a link with ``http``, however, for accessing the link securely, ``https`` is usually recommendded.
Details for setting up __https__ with **BSIS** can be found `here <https://shiny-aws-doc.readthedocs.io/en/latest/Https.html>`_