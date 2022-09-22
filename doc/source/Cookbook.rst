Cookbook
=============

This page provides an **end-to-end** instruction about how to deploy ``hello_world`` shiny application using **BSIS** and **ASIS**


Step 1: Create a customized AMI (optional):
"""""""""
Optionally, we can create a customized AMI to **pre-install** all the required dependancies.

1.1: Bring up an instance with all dependancies
***********

First we need to bring up an instance (with the all needed dependancies defined in ``cloud-init.sh``). A script for doing so can be found in ``etc/scripts/create_base.py``.
Please update ``cloud_init`` (user data), ``spot_spec_path`` (instance defination) and ``spot_price`` (the price you are willing to pay) accrodingly.

.. code-block:: bash

    cloud_init = "etc/scripts/cloud-init.sh"
    spot_spec_path = "etc/scripts/spot_spec.json"
    spot_price = 0.1


.. note::

    In order to create your own AMI, for **BSIS** you will need to ask your AWS administor to provide ``SecurityGroupIds`` and ``SubnetId``. A base AMI (e.g., a Basic Linux AMI from AWS) is also needed.
    All of these should be configured within ``spot_spec.json``

1.2: Make an AMI
***********

After we have an instance running with all the dependancies, we can use ``etc/scripts/create_ami.py`` to make an AMI. In order to do so, the following paramters are to be adjusted:

.. code-block:: bash

    instance_id = "id-12312312"
    ami_name = "shiny_aws_ami"

where ``instance_id`` represents the instance that being brought up at `Step 1.1`, and ``ami_name`` is your AMI ID to be used on AWS.


Step 2: Shiny application on S3
"""""""""

2.1: Create a shiny app locally:
***********
First we need to create a shiny application, and test it locally. 

In this tutorial, the application is called ``hello_world``. An example can be obtained from ``etc/examples/hello_world``. 

.. note::

    Note that you need to update the **<S3 path>** in ``cloud-init.sh``. For example, orginially it is ``s3://xxxx-shiny-app/r/hello_world/``, you need to update it to something that is relevant to your application

2.2: Upload the shiny app:
***********
Then the Shiny application can be uploaded to S3 using ``etc/scripts/copy_shiny.py``. You need to update/configure the following two parameters in the script based on your shiny application:

.. code-block:: bash

    shiny_app_local = "etc/examples/hello_world"
    shiny_app_s3 = "s3://xxxx-shiny-app/r/"

where ``shiny_app_local`` is the place where your application sits locally, and ``shiny_app_s3`` is where the application to be uploaded (it must be consistent with **<S3 path>** in `Section 2.1`)
