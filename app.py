#!/usr/bin/env python3
import os
from aws_cdk import App, Environment

from cdk_glue_python_yellowtaxi.cdk_glue_python_yellowtaxi_stack import CdkGluePythonYellowtaxiStack


app = App()
                             
prod_env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), 
                             region=os.getenv('CDK_DEFAULT_REGION'))

stage_env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), 
                             region='us-west-2')


print(f"Stage Environment: Account={os.getenv('CDK_DEFAULT_ACCOUNT')}, Region={os.getenv('CDK_DEFAULT_REGION')}")
print(f"Prod Environment: Account={os.getenv('CDK_DEFAULT_ACCOUNT')}, Region={os.getenv('CDK_DEFAULT_REGION')}")


CdkGlueRayYellowtaxiStack(app, "CdkGlueYellowtaxiStack-Stage", env=stage_env)
CdkGlueRayYellowtaxiStack(app, "CdkGlueYellowtaxiStack-Prod", env=prod_env)

# Synthesize the app
app.synth()