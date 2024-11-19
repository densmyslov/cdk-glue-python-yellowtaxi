import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_glue_python_yellowtaxi.cdk_glue_python_yellowtaxi_stack import CdkGluePythonYellowtaxiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_glue_python_yellowtaxi/cdk_glue_python_yellowtaxi_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkGluePythonYellowtaxiStack(app, "cdk-glue-python-yellowtaxi")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
