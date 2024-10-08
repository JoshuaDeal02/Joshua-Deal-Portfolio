import boto3
import json

def create_role():
    iam = boto3.client('iam')
    role_name = 'newRole'
    #The trust policy document is an example, the user could input a different json file instead for actual use
    trust_policy = {
        "Version":"2012-10-17",
        "Statement":[
            {
                "Effect":"Allow",
                "Principal":{
                    "Service":"ec2.amazonaws.com"
                },
                "Action":"sts:AssumeRole"
            }
        ]

    }
    iam.create_role(RoleName = role_name, AssumeRolePolicyDocument = json.dumps(trust_policy))

create_role()