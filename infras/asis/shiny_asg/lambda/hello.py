import boto3

client = boto3.client('autoscaling')


def lambda_handler(event, context):
    print("xxx")
    """
    response = client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[
            "asg_test",
        ],
        MaxRecords=50
    )
    instances = response['AutoScalingGroups'][0]['Instances']
    for i in range(len(instances)):
      print(instances[i]['InstanceId'])
    """
