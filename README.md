# A scalable Shiny infrastructure on AWS

The system helps to construct an AWS based infrastructure for hosting [Shiny](https://shiny.rstudio.com/) applications:
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

The documentation for the system can be found [here](https://shiny-aws-doc.readthedocs.io/en/latest/BSIS.html)