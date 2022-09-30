ASIS
=====

This page describes how to deploy a **ASIS** infrastructure.

All the permissions from **ASIS** can be automatically set up, so actually implementing **ASIS** could be simpler than **BSIS**.
An **ASIS** can be implemented as:

.. code-block:: bash

   start_asis --workdir <WORKING DIRECTORY> 
              --ami <AMI ID>
              --region <AWS REGION> 
              [--cdk <ASIS CDK DIRECTORY>]
              [--uuid <STACK UNIQUE ID>]
              [--zone <ZONE INFORMATION>]
              [--create_zone]

where ``--workdir`` is the working directory (where the source `ASIS CDK` will be copied to), ``ami`` is the AMI ID for the base image 
and ``region`` represents the AWS region to be used.

Optionally, we can provide the source `ASIS CDK` directory (via ``--cdk``), and the unique ID ``--uuid``.
Also, we can choose whether we want to create a new hosted zone (e.g., by setting ``--create_zone``) in `Route 53` or use an existing one. 
The zone information should be defined in ``--zone``.

For example, ``start_asis --workdir /tmp/asis --ami ami-12345 --region us-west-2 --cdk infras/asis/shiny_asg --uuid r-shiny-asg --zone (xxx.com, Z123abc) --create_zone``

**It is worthwhile to note that it might take quite a while for Route 53 traffic to be updated, before that we should use the Application Load Balancer DNS to access the Shiny application**

.. note::

   1. Note that there is an additional prefix ``dualstack`` added in the **Hosted zones -> Record** of **Route53**. 
       
       For example:

           - in ``EC2 Load Balancer``, the ``DNS`` is ``Shiny-shiny-18HWQ7XESTMT7-1561701960.ap-southeast-2.elb.amazonaws.com``
           - However in ``Hosted zones -> Record``, the route traffic is ``dualstack.shiny-shiny-18hwq7xestmt7-1561701960.ap-southeast-2.elb.amazonaws.com.``
   
       Therefore, in some cases, we need to go to **Hosted zones -> Record** of **Route53**, and manually remove ``dualstack``

   2. When we create a new hosted domain, there can be mismatch of the **domain servers** between the ``registered domain`` and ``the Hosted zones``. 
      The details can be found at `here <https://stackoverflow.com/questions/35969976/amazon-aws-route-53-hosted-zone-does-not-work>`_