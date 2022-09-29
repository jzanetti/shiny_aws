ASIS
=====

This page describes how to deploy a **ASIS** infrastructure.

All the permissions from **ASIS** can be automatically set up, so actually implementing **ASIS** could be simpler than **BSIS**.
An **ASIS** can be implemented as:

.. code-block:: bash

   start_asis --workdir <WORKING DIRECTORY> --domain <DOMAIN NAME> --ami <AMI ID> --region <AWS REGION> [--cdk <ASIS CDK DIRECTORY>] [--uuid <STACK UNIQUE ID>]

where ``--workdir`` is the working directory (where the source `ASIS CDK` will be copied to), ``domain`` represents the domain name
to be used (e.g., defined by `Route 53`). ``ami`` is the AMI ID for the base image and ``region`` represents the AWS region to be used.
Optionally, we can provide the source `ASIS CDK` directory, and the unique ID ``--uuid``.

For example, ``start_asis --workdir /tmp/asis --cdk infras/asis/shiny_asg --domain www.mot-dev.link --uuid r-shiny-asg``

**It is worthwhile to note that it might take quite a while for Route 53 traffic to be updated, before that we should use the Application Load Balancer DNS to access the Shiny application**

.. note::

   Step 1. Note that due the **bug** in `cdk`, there is an additional prefix ``dualstack`` added in the **Hosted zones -> Record** of **Route53**. 
       
       For example:

           - in ``EC2 Load Balancer``, the ``DNS`` is ``Shiny-shiny-18HWQ7XESTMT7-1561701960.ap-southeast-2.elb.amazonaws.com``
           - However in ``Hosted zones -> Record``, the route traffic is ``dualstack.shiny-shiny-18hwq7xestmt7-1561701960.ap-southeast-2.elb.amazonaws.com.``
   
       Therefore, in this case, we need to go to **Hosted zones -> Record** of **Route53**, and manually remove ``dualstack``

   Step 2. There can be mismatch of the **domain servers** between the ``registered domain`` and ``the Hosted zones``. 
      The details can be found at `here <https://stackoverflow.com/questions/35969976/amazon-aws-route-53-hosted-zone-does-not-work>`_

   Note that we need strickly following the order of the above steps.