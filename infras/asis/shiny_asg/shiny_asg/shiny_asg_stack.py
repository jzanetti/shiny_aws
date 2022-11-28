import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_cloudwatch as cw
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam
import aws_cdk.aws_sqs as sqs
from aws_cdk import Stack  # Duration,; aws_sqs as sqs,
from aws_cdk import App, CfnOutput, Duration, RemovalPolicy
from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_autoscaling_hooktargets as hooktargets
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_route53, aws_route53_targets
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subscriptions
from aws_cdk.aws_cloudwatch_actions import AutoScalingAction
from constructs import Construct
from aws_cdk.aws_certificatemanager import Certificate


class ShinyAsgStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        self.__config = config

        # ------------------------------
        # Step 1: create VPC and SG
        # ------------------------------
        vpc = self.__create_vpc()
        sg = self.__get_sg(vpc)
        ssl = self.__get_ssl()

        # ------------------------------
        # Step 2: create ASG and Load balancer
        # ------------------------------
        userData = self.__get_userdata()
        asg = self.__create_asg(vpc, sg, userData)
        lb = self.__create_load_balancer(vpc, asg, sg, ssl)

        # ------------------------------
        # Step 3: connect LB to route 53
        # ------------------------------
        if self.__config["route53"]["zone"]["create_new"]:
            zone = self.__create_hosted_zone()
        else:
            zone = self.__query_hosted_zone()

        self.__create_a_record(lb, zone)


    def __get_ssl(self):
        return Certificate.from_certificate_arn(
            self, 
            id=self.__apply_status_and_region(self.__config["ssl"]["id"]), 
            certificate_arn=self.__config["ssl"]["arn"])

    def __create_a_record(self, lb, zone):

        aws_route53.ARecord(
            self, 
            self.__apply_status_and_region(self.__config["route53"]["record"]["id"]),
            record_name=self.__config["route53"]["record"]["name"], 
            zone=zone, 
            target=aws_route53.RecordTarget.from_alias(aws_route53_targets.LoadBalancerTarget(lb))
        )


    def __query_hosted_zone(self):
        return aws_route53.HostedZone.from_hosted_zone_attributes(
            self,
            id = self.__apply_status_and_region(self.__config["route53"]["zone"]["id"]), 
            hosted_zone_id = self.__config["route53"]["zone"]["zone_id"],
            zone_name = self.__config["route53"]["zone"]["zone_name"])


    def __create_hosted_zone(self):
        return aws_route53.PublicHostedZone(
            self, 
            self.__apply_status_and_region(self.__config["route53"]["zone"]["zone_id"]),
            zone_name=self.__apply_status_and_region(self.__config["route53"]["zone"]["zone_name"]))

    def __get_userdata(self):
        data = open("./cloud-init.sh", "rb").read()
        userData = ec2.UserData.for_linux()
        userData.add_commands(str(data,'utf-8'))
        return userData

    def __get_sg(self, vpc):
        sg = ec2.SecurityGroup(
            self, 
            id=self.__apply_status_and_region(self.__config["sg"]["asg"]["id"]),
            security_group_name=self.__apply_status_and_region(self.__config["sg"]["asg"]["name"]),
            allow_all_outbound=True,
            vpc=vpc)

        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="http",
        )

        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="ssh",
        )

        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(), 
            connection=ec2.Port.tcp(443), 
            description="https")

        return sg

    def __create_vpc(self):
        return ec2.Vpc(
            self,
            self.__apply_status_and_region(self.__config["vpc"]["id"]),
            max_azs=self.__config["vpc"]["max_azs"],
            cidr=self.__config["vpc"]["cidr"],
            subnet_configuration=[ec2.SubnetConfiguration(
                subnet_type=ec2.SubnetType.PUBLIC,
                name=self.__apply_status_and_region(self.__config["vpc"]["subnet"]),
            )],
            )

    def __create_asg(self, vpc, sg, user_data):

        role = iam.Role(
            self, 
            self.__apply_status_and_region(self.__config["asg"]["role"]["id"]),
            role_name=self.__apply_status_and_region(self.__config["asg"]["role"]["name"]),
            description="Allow ASG to interact with S3",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
                ]
        )

        linux_ami = ec2.GenericLinuxImage({
            self.__config["common"]["region"]: self.__config["common"]["ami"],
        })

        asg = autoscaling.AutoScalingGroup(
            self, 
            self.__apply_status_and_region(self.__config["asg"]["id"]),
            auto_scaling_group_name=self.__apply_status_and_region(
                self.__config["asg"]["name"]),
            role=role,
            vpc=vpc,
            instance_type=ec2.InstanceType(instance_type_identifier=self.__config["common"]["instance_type"]),
            machine_image=linux_ami,
            key_name=self.__config["asg"]["key_name"],
            security_group=sg,
            desired_capacity=self.__config["asg"]["capacity"]["desired"],
            max_capacity=self.__config["asg"]["capacity"]["max"],
            min_capacity=self.__config["asg"]["capacity"]["min"],
            user_data=user_data,
            spot_price=str(self.__config["common"]["spot_price"])
            )

        asg.scale_on_cpu_utilization(
            self.__apply_status_and_region(self.__config["asg"]["policy"]["id"]),
            target_utilization_percent=self.__config["asg"]["policy"]["target_utilization_percent"],
            cooldown=Duration.seconds(self.__config["asg"]["policy"]["cooldown"])
        )

        return asg

    def __create_load_balancer(self, vpc, asg, sg, ssl):
        lb = elbv2.ApplicationLoadBalancer(
            self, 
            self.__apply_status_and_region(self.__config["lb"]["id"]),
            vpc=vpc,
            security_group=sg,
            internet_facing=True)

        listener = lb.add_listener("Listener2", port=443)
        listener.add_targets("Target", port=80, targets=[asg])

        listener.add_certificates(self.__apply_status_and_region(
            self.__config["ssl"]["certificate"]), certificates=[ssl])
        listener.connections.allow_default_port_from_any_ipv4(
            "Open this LB to the public")
        CfnOutput(self,"LoadBalancer", export_name="LoadBalancer", value=lb.load_balancer_dns_name)
        return lb

    def __apply_status_and_region(self, str_input):
        return str_input.format(
            # status=self.__config["common"]["status"],
            region=self.__config["common"]["region"],
            uuid=self.__config["common"]["uuid"]
        )
