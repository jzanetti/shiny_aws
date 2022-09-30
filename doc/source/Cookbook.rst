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

.. note::

    After the AMI being made, please remember to terminate the instance from `Step 1.1`

Details about making an customized AMI can be accessed `here <https://shiny-aws-doc.readthedocs.io/en/latest/Customized_AMI.html>`_

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

    python copy_shiny.py --src etc/examples/hello_world --dest_dir s3://xxxx-shiny-app/r/

where ``src`` is the place where your application sits locally, and ``dest_dir`` is where the application to be uploaded (it must be consistent with **<S3 path>** in `Section 2.1`)

Details about creating a Shiny application for **SHINY_AWS** can be accessed `here <https://shiny-aws-doc.readthedocs.io/en/latest/Shiny.html>`_

Step 3: Bring up the Shiny online
"""""""""

As we discussed before, there are two ways that you can bring up a shiny application online: **BSIS** and **ASIS**. 
For general development purpose, using **BSIS** is recommended, while **ASIS** should be adopted for operational usage.

3.1: Using BSIS
***********
Before we start a BSIS infrastructure, please make sure that you have the following ready:

- A customized AMI or the basic AWS linux AMI (made by `Step 1`, see details from `here <https://shiny-aws-doc.readthedocs.io/en/latest/Customized_AMI.html>`_)
- A Shiny application being uploaded to S3 (made by `Step 2`, with four compulsary components listed in `Shiny Application <https://shiny-aws-doc.readthedocs.io/en/latest/Shiny.html>`_).
- A private key for accessing EC2 (see details `here <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html>`_)
- AWS related information such as ``SecurityGroupIds``, ``SubnetId`` and ``IamInstanceProfile``, which can be obtained from your AWS administor.
- Optionally, you can have your Elastic IP or authentications if you have them

Here we use an example **BSIS** configuration (at ``etc/cfg/bsis.yml``) to bring up the instance. 

.. code-block:: bash

    conda activate shiny_aws
    start_bsis --cfg etc/cfg/bsis.yml --workdir /tmp/bsis_exp

Note that you will need to update ``etc/cfg/bsis.yml`` accordingly based on your own circumstance (e.g., the 5 elements listed above).

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