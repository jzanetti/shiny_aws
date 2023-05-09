ASIS
=====

This page describes how to deploy a **ASIS** infrastructure.

ASIS deployment from scratch
------

All the permissions from **ASIS** can be automatically set up, so actually implementing **ASIS** could be simpler than **BSIS**.
An **ASIS** can be implemented as:

.. code-block:: bash

    start_asis
            --workdir <WORKING DIRECTORY> 
            --cfg <ASIS CONFIGURATION>


where ``--workdir`` is the working directory (where the source `ASIS CDK` will be copied to), ``cfg`` is the ASIS configuration file

The configuration for **ASIS** is similar to **BSIS**, while it only contains two sessions ``shiny`` and ``aws``.

The ``shiny`` session contains the information about where is the shiny application repository (and the credentials to access it if needed). 
``aws`` includes the base image ``AMI``, ``region`` and ``route53`` setup if we need it.

An simple example is shown below:

.. code-block:: bash

    shiny: 
        names: 
            hello_world_1: hello_world/link1
            hello_world_2: hello_world/link2
        url: https://gitlab.com/test-12345/mot_shiny_dev.git
        branch: main
        cred:
            user: <user name>
            token: <token>

    aws: 
        ami: ami-xxxxx
        region: ap-southeast-2
        route53:
            create_new: false
            domain_name: test.come
            zone_id: Zxxx-yyy-zzzz

ASIS deployment from an AMI
------
When it comes to handling fluctuating traffic volumes for a Shiny application, **ASIS** offers a distinct advantage over **BSIS** with its scaling option.
However, initializing a new server requires time to "warm up," including installing all dependencies, which can be a lengthy process.

To avoid the time-consuming server "warm up" process during production deployment, it is recommended to deploy **ASIS** from an existing AMI.

- Step 1: Deploy the application(s) via **BSIS** (e.g., see `here <https://shiny-aws-doc.readthedocs.io/en/latest/BSIS.html#deployment>`_). Note that if you have multiple Shiny applications, it is recommended to bundle them together in the same **BSIS** deployment.
- Step 2: Once you have tested **BSIS** and confirmed that everything is working correctly, create an AMI of the EC2 instance using the following command: ``app_utils --job makeami --name <SHINY APPLICATION NAME>``, where ``SHINY APPLICATION NAME`` refers to the name of the application for which **BSIS** was set up.
- Step 3: Once the AMI is made (it could take 10-15 minutes), the original **BSIS** can be shutdown, and the **ASIS** can be brought up using the configuration as below:

        .. code-block:: bash

            shiny: null

            aws: 
                ami: ami-xxxxx
                region: ap-southeast-2
                route53:
                    create_new: false
                    domain_name: test.come
                    zone_id: Zxxx-yyy-zzzz

        Where ``ami-xxxxx`` is the AMI-ID just being built.


**It is worthwhile to note that it might take quite a while for Route 53 traffic to be updated, before that we should use the Application Load Balancer DNS to access the Shiny application**

.. note::

   1. Note that there is an additional prefix ``dualstack`` added in the **Hosted zones -> Record** of **Route53**. 
       
       For example:

           - in ``EC2 Load Balancer``, the ``DNS`` is ``Shiny-shiny-18HWQ7XESTMT7-1561701960.ap-southeast-2.elb.amazonaws.com``
           - However in ``Hosted zones -> Record``, the route traffic is ``dualstack.shiny-shiny-18hwq7xestmt7-1561701960.ap-southeast-2.elb.amazonaws.com.``
   
       Therefore, in some cases, we need to go to **Hosted zones -> Record** of **Route53**, and manually remove ``dualstack``

   2. When we create a new hosted domain, there can be mismatch of the **domain servers** between the ``registered domain`` and ``the Hosted zones``. 
      The details can be found at `here <https://stackoverflow.com/questions/35969976/amazon-aws-route-53-hosted-zone-does-not-work>`_