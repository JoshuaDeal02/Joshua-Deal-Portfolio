import boto3

def detach_policy(policy_arn, target, type):
    iam = boto3.client('iam')

    if type == 'user':
        response = iam.detach_user_policy(UserName = target, PolicyArn = policy_arn)
    
    elif type == 'group':
        response = iam.detach_group_policy(GroupName = target, PolicyArn = policy_arn)
    print(response)

type = input("Would you like to detach the policy from a \'user\' or a \'group\'?")
if type == 'user':
    target = input("Enter the target user name: ")
elif type == 'group':
    target = input("Enter the target group name: ")
else:
    print('You must enter either \'user\' or \'group\'')
    exit()
policy_arn = input("Enter the arn of the policy to be detached: ")

detach_policy(policy_arn, target, type)
