import aws_cdk as core
import aws_cdk.assertions as assertions

from shiny_asg.shiny_asg_stack import ShinyAsgStack

# example tests. To run these tests, uncomment this file along with the example
# resource in shiny_asg/shiny_asg_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ShinyAsgStack(app, "shiny-asg")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
