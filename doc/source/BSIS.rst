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

For **shiny**, we need to define where the Shiny application comes from. Note that all Shiny applications used in **BSIS** must be uploaded to S3 beforehand. How to create a Shiny on S3 can be obtained `here <https://shiny-aws-doc.readthedocs.io/en/latest/Shiny.html>`_.

An simple example is given below:

.. code-block:: bash

   shiny: 
      name: hello_world
      s3: s3://xxxxxxx-shiny-app/r
      userdata: cloud-init.sh

The above provides some basic shiny information. The instance will be brought up by using the user data ``cloud-init.sh``, 
and the shiny application from ``s3://xxxxxxx-shiny-app/r/hello_world``.

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


Note that we will have to provide a few **user** defined parameters:

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