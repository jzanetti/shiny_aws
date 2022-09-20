Welcome to SHINY_AWS
===================================

**SHINY_AWS** is to help easily constructing an AWS based infrastructure for hosting `Shiny <https://shiny.rstudio.com/>`_ applications:

- the Basic Shiny Infrastructure Suite (BSIS) which contains:
   - An EC2 instance (from spot market or on-demand)
   - Shiny application
   - Optional: attaching an Elastic IP address
   - Optional: Authentication based on `nginx`

- the Advanced Shiny Infrastructure Suite (ASIS) which contains:
   - Autoscaling group with EC2
   - Application load balancer
   - Shiny application
   - Optional: Customized DNS using Route 53

The main difference between BSIS and ASIS is that ASIS is able to scale out the number of instances when the shiny server becomes busy (e.g., suddenly there are more people hit the website), and scale in when the resources are not required.

BSIS is usually used for development purpose (e.g., the scaling is not a big issue, and there are existing security groups, subnets etc. that can be shared by multiple developers). ASIS is recommended for production deployment while we want a relatively isolated while scalable working environment (e.g., ASIS creates and manages its own permissions).

Besides the above noted services 

An `hello_world` example is used to demostrate the usage for this system.

.. note::

   Any issues/suggestions for this system please go to zhans@transport.govt.nz


Contents
--------

.. toctree::

   Basics
   Nix_derivation
   Build_nix
   Proj_manage
   flakes