Welcome to SHINY_AWS
===================================

.. image:: shiny_aws_logo.PNG
   :width: 600

**SHINY_AWS** is an open-source repository that constructs an cloud (AWS) based infrastructure for hosting `Shiny <https://shiny.rstudio.com/>`_ applications (or potentially any visualization & analytical interactive UI applications). 
There are two suites in the repository:

- the Basic Shiny Infrastructure Suite (BSIS):
   - An EC2 instance (from spot market or on-demand)
   - Shiny application
   - Optional: an Elastic IP address
   - Optional: Authentication based on `nginx`

- the Advanced Shiny Infrastructure Suite (ASIS):
   - Autoscaling Group with EC2
   - Application Load Balancer
   - Shiny application
   - Optional: DNS using `Route 53`

The main difference between **BSIS** and **ASIS** is that **ASIS** is able to 
scale out resources (e.g., the number of CPUs) when the backend server becomes busy (e.g., suddenly there are more hits on the website), and scale in when the resources are not required.

**BSIS** is usually used for development purpose (e.g., the scaling is not a big issue, and there are existing security groups, subnets etc. that can be shared by multiple developers). 
**ASIS** is recommended for production deployment where we want a relatively isolated and scalable working environment (e.g., **ASIS** can create and manage its own permissions).

An `hello_world` example is used to demostrate the usage for this system.

.. note::

   Any issues/suggestions for this system please go to **Sijin ZHANG** at zsjzyhzp@gmail.com


Contents
--------

.. toctree::

   Installation
   Shiny
   BSIS
   ASIS
   Customized_AMI
   Cookbook