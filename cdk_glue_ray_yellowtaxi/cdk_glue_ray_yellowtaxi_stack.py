from aws_cdk import (
                        Stack,
                        aws_s3 as s3,
                        RemovalPolicy,
                        aws_iam as iam,
                        CfnOutput,
                        aws_glue as glue,
                        aws_s3_assets as s3_assets
                    )
from constructs import Construct

class CdkGlueRayYellowtaxiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env_name = self.node.try_get_context("env_name") or "stage"
        env_config = self.node.try_get_context("env")[env_name]

#################################################################################
# S3 Bucket (Step 1)
################################################################################
        # get bucket_name depending on environment
        bucket_name = env_config.get("bucket_name")
        if not bucket_name:
            raise ValueError(f"bucket_name is not defined for environment: {env_name}")
        
        # Create the S3 bucket
        bucket = s3.Bucket(self, "MyBucket",
            bucket_name=bucket_name,
            removal_policy=RemovalPolicy.DESTROY,  # Optional: for testing only; use RETAIN for prod
            auto_delete_objects=True  # Optional: for testing only
        )

#########################################################################################
# IAM Role for Glue (Step 2)
#########################################################################################


        # Create an IAM role for Glue with Ray
        glue_ray_role = iam.Role(
            self, "GlueRayJobRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            description="Role for Glue job running Ray",
        )

        # Attach managed policies needed by Glue
        glue_ray_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole")
        )
        # Create and attach an inline policy for custom permissions
        # to read files from nyc-tlc bucket
        glue_ray_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "s3:GetObject",
            ],
            resources=["arn:aws:s3:::nyc-tlc/*"]
        ))
        glue_ray_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "s3:PutObject",
            ],
            resources=[f"arn:aws:s3:::{bucket_name}/*"]
        ))

        # Output the role ARN for reference
        CfnOutput(self, "GlueRayRoleArn", value=glue_ray_role.role_arn, description="The ARN of the Glue Ray job IAM Role")

#########################################################################################
# Glue Job (Step 3)
#########################################################################################
        # Upload the Glue job script to S3
        glue_script_asset = s3_assets.Asset(self, "GlueRayJobScript",
            path="scripts/glue_ray_job.py"
        )
        
        # Create a Glue Job
        glue.CfnJob(
            self, "GlueRayJob",
            role=glue_ray_role.role_arn,
            command=glue.CfnJob.JobCommandProperty(
                name="glueetl",
                python_version="3",
                script_location=f"s3://{bucket_name}/glue/scripts/glue_ray_job.py"  # Adjust the script location accordingly
            ),
            glue_version="4.0",  # Glue 4.0 supports Ray
            worker_type="G.1X",
            number_of_workers=2,  # Adjust based on the size of your dataset
            description="AWS Glue job for processing data using Ray",
            default_arguments={
                "--bucket_name": bucket_name
            }
        )
