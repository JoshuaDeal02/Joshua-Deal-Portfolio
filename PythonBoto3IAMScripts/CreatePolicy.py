import boto3
import json

def create_policy(name, effect, action, resource):
    iam = boto3.client('iam')

    policy = {
        "Version":"2012-10-17",
        "Statement":[
            {
            "Effect":effect,
            "Action":action,
            "Resource":resource
            }
        ]
    }

    response = iam.create_policy(PolicyName = name, PolicyDocument = json.dumps(policy))

    print(response)
    
name = input('Enter the name of the new policy: ')
effect = input('Enter the effect of the policy: ')
action = input('Enter the action of the policy: ')
resource = input('Enter the resource the policy refers to: ')

create_policy(name, effect, action, resource)