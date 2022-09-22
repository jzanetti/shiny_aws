Cookbook
=============

This page provides an **end-to-end** instruction about how to deploy ``hello_world`` shiny application using **BSIS** and **ASIS**

Step 1: Make the shiny application locally, and upload it to S3
***********
First we need to create a shiny application, and test it locally. 

In this tutorial, the application is called ``hello_world``. An example can be obtained from ``etc/examples/hello_world``. 

.. note::

    Note that you need to update the **<S3 path>** in ``cloud-init.sh``. For example, orginially it is ``s3://xxxx-shiny-app/r/hello_world/``, you need to update it to something that relevant to your application

Then the Shiny application can be uploaded to S3 using ``copy_shiny.py``. You need to update/configure the following two parameters in the script based on your shiny application:

.. code-block:: bash

    shiny_app_local = "etc/examples/hello_world"
    shiny_app_s3 = "s3://xxxx-shiny-app/r/"