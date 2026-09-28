from aws_cdk import Stack
from aws_cdk import aws_s3 as s3, aws_dynamodb as dynamodb, aws_ecr as ecr, aws_ecs as ecs, aws_ec2 as ec2
from constructs import Construct

class DemandSensingStack(Stack):
    def __init__(self,scope:Construct,id:str,**kwargs):
        super().__init__(scope,id,**kwargs)
        s3.Bucket(self,"DataBucket",versioned=True,encryption=s3.BucketEncryption.S3_MANAGED)
        dynamodb.Table(self,"Jobs",partition_key=dynamodb.Attribute(name="job_id",type=dynamodb.AttributeType.STRING),billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST)
        vpc=ec2.Vpc(self,"Vpc",max_azs=2,nat_gateways=1)
        ecs.Cluster(self,"Cluster",vpc=vpc)
        ecr.Repository(self,"Repository",repository_name="demand-sensing-agent")
