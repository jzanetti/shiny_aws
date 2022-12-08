Cookbook
=============

This page provides an **end-to-end** instruction about how to deploy ``hello_world`` shiny application using **BSIS** and **ASIS**


Step 1: Load the environment:
"""""""""
First we need to load the **SHINY_AWS** working environment:

.. code-block:: bash

    conda activate shiny_aws

Step 2 (optional): Create a customized AMI:
"""""""""
Optionally, we can create a customized AMI to **pre-install** all the required dependancies. The command is:

.. code-block:: bash

    make_base --cloud_init etc/aws/cloud-init.sh --spot_spec etc/aws/spot_spec.json --ami_name ami_test_v2.0 --expected_duration 30 --overwrite_ami

The above will create an AMI with name ``ami_test_v2.0``.

.. note::

    In order to create your own AMI, you will need to ask your AWS administor to provide ``SecurityGroupIds`` and ``SubnetId``. A base AMI (e.g., a Basic Linux AMI from AWS) is also needed.
    All of these should be configured within ``spot_spec.json``

Details about making an customized AMI can be accessed `here <https://shiny-aws-doc.readthedocs.io/en/latest/Customized_AMI.html>`_


Step 3: Shiny application on AWS
"""""""""

3.1: Create a shiny app locally:
***********
First we need to create a shiny application, and test it locally. 

In this tutorial, the application is called ``hello_world``. 
After we test it locally, we should upload it to a remote __GIT__ repository. An example can be found `here <https://github.com/jzanetti/shiny_aws_examples>`_

There are three components in this application:

.. code-block:: bash

    - cloud-init.sh
    - server.R
    - ui.R

Details about creating a Shiny application for **SHINY_AWS** can be accessed `here <https://shiny-aws-doc.readthedocs.io/en/latest/Shiny.html>`_

As we discussed before, there are two ways that we can bring up a shiny application online: **BSIS** and **ASIS**. 
For general development purpose, using **BSIS** is recommended, while **ASIS** should be adopted for operational usage.

3.2: Using BSIS
***********

Before we start a BSIS infrastructure, please make sure that you have the following ready:

- A customized AMI or the basic AWS linux AMI (made by **Step 1**, see details from `here <https://shiny-aws-doc.readthedocs.io/en/latest/Customized_AMI.html>`_)
- A Shiny application is uploaded to a remote Git repository (made by **Step 2**, see details in `Shiny Application <https://shiny-aws-doc.readthedocs.io/en/latest/Shiny.html>`_).
- A private key for accessing EC2 (see details `here <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html>`_)
- AWS related information such as ``SecurityGroupIds``, ``SubnetId`` and ``IamInstanceProfile``, which can be obtained from your AWS administor.
- Optionally, you can have your Elastic IP or authentications if you have them

Here we use an example **BSIS** configuration (at ``etc/cfg/bsis.yml``) to bring up the instance. 

.. code-block:: bash

    start_bsis --cfg etc/cfg/bsis.yml --workdir /tmp/bsis_exp

Note that we will need to update the following parameters in ``etc/cfg/bsis.yml`` (within the ``aws`` section):

- ``ImageId``: the base Image ID (created by **Step 1**)
- ``KeyName``: the private key to access EC2
- ``SecurityGroupIds``: Security group ID (can be obtained from AWS administor)
- ``SubnetId``: Subnet ID (can be obtained from AWS administor)
- ``IamInstanceProfile``: IAM profile for Shiny (can be obtained from AWS administor)

After this we should be able to view our Shiny application either though the automatically assigned public IP or the elastic IP defined in ``bsis.yml``. 
We can use the provided `Utilities <https://shiny-aws-doc.readthedocs.io/en/latest/Utilities.html>`_ to obtain the IP address.

.. note::

    Note that it is always a good practice to set the lifespan for the shiny application in ``bsis.yml``. If not, please remember to terminate the server when you don't need it anymore.

3.3: Using ASIS
***********
Running **ASIS** is much easier than **BSIS**, while you would need to have your **Route 53** domain ready.

Here is an example of setting up **BSIS**:

.. code-block:: bash

    export CDK_PATH=shiny_aws/infras/asis/shiny_asg
    start_asis --workdir /tmp/asis --cfg etc/cfg/asis.yml

Similar to **BSIS**, we will need to adjust the ``aws`` section within ``etc/cfg/asis.yml``:

- ``ami``: the base Image ID (created by **Step 1**)
- ``region``: the AWS region to be used
- ``route53``: Route 53 information including the ``domain_name`` and ``zone_id``

After this we should be able to view our Shiny application from the path defined in ``domain_name`` (Details can be found in `here <https://shiny-aws-doc.readthedocs.io/en/latest/ASIS.html>`_)