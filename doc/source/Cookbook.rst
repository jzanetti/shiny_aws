Cookbook
=============

This page provides an **end-to-end** instruction about how to deploy ``hello_world`` shiny application using **BSIS** and **ASIS**


Step 1 (optional): Create a customized AMI:
"""""""""
Optionally, we can create a customized AMI to **pre-install** all the required dependancies. The command is:

.. code-block:: bash

    conda activate shiny_aws
    make_base --cloud_init etc/aws/cloud-init.sh --spot_spec etc/aws/spot_spec.json --ami_name ami_test_v2.0 --expected_duration 30 --overwrite_ami

The above will create an AMI with name ``ami_test_v2.0``.

.. note::

    In order to create your own AMI, you will need to ask your AWS administor to provide ``SecurityGroupIds`` and ``SubnetId``. A base AMI (e.g., a Basic Linux AMI from AWS) is also needed.
    All of these should be configured within ``spot_spec.json``

Details about making an customized AMI can be accessed `here <https://shiny-aws-doc.readthedocs.io/en/latest/Customized_AMI.html>`_


Step 2: Shiny application on S3
"""""""""

2.1: Create a shiny app locally:
***********
First we need to create a shiny application, and test it locally. 

In this tutorial, the application is called ``hello_world``. After we test it locally, we should upload it to a remote _GIT_ repository. An example can be found `here <https://github.com/jzanetti/shiny_aws_examples>`_

Details about creating a Shiny application for **SHINY_AWS** can be accessed `here <https://shiny-aws-doc.readthedocs.io/en/latest/Shiny.html>`_

Step 3: Bring up the Shiny online
"""""""""

As we discussed before, there are two ways that you can bring up a shiny application online: **BSIS** and **ASIS**. 
For general development purpose, using **BSIS** is recommended, while **ASIS** should be adopted for operational usage.

3.1: Using BSIS
***********
Before we start a BSIS infrastructure, please make sure that you have the following ready:

- A customized AMI or the basic AWS linux AMI (made by **Step 1**, see details from `here <https://shiny-aws-doc.readthedocs.io/en/latest/Customized_AMI.html>`_)
- A Shiny application being uploaded to a remote Git repository (made by **Step 2**, see details in `Shiny Application <https://shiny-aws-doc.readthedocs.io/en/latest/Shiny.html>`_).
- A private key for accessing EC2 (see details `here <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html>`_)
- AWS related information such as ``SecurityGroupIds``, ``SubnetId`` and ``IamInstanceProfile``, which can be obtained from your AWS administor.
- Optionally, you can have your Elastic IP or authentications if you have them

Here we use an example **BSIS** configuration (at ``etc/cfg/bsis.yml``) to bring up the instance. 

.. code-block:: bash

    conda activate shiny_aws
    start_bsis --cfg etc/cfg/bsis.yml --workdir /tmp/bsis_exp

Note that you will need to update ``etc/cfg/bsis.yml`` accordingly.

After this we should be able to view our Shiny application either though the automatically assigned public IP or the elastic IP defined in ``bsis.yml``.

.. note::

    Note that it is a good practice to set the lifespan for the shiny application in ``bsis.yml``. If not, please remember to terminate the server when you don't need it anymore.

3.2: Using ASIS
***********
Running **ASIS** is much easier than **BSIS**, while you would need to have a **Route 53** domain ready.

Here is an example of setting up **BSIS**:

.. code-block:: bash

    conda activate shiny_aws
    export CDK_PATH=shiny_aws/infras/asis/shiny_asg
    start_asis --workdir /tmp/asis --ami ami-06618c31796bff2cb --region ap-southeast-2 --cdk $CDK_PATH --uuid hello-world-test --zone '(mot-dev.link, Z0778680205QCZAT4YE40)'

Note that the above will use an existing hosted zone (name: ``mod-dev.link``, ID: ``Z0778680205QCZAT4YE40``).

After this we should be able to view our Shiny application at ``www.mot.link`` (Details can be found in `here <https://shiny-aws-doc.readthedocs.io/en/latest/ASIS.html>`_)