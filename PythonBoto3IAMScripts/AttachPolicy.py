import boto3

def attach_policy(policy_arn, target, type):
    iam = boto3.client("iam")

    if type == 'user':
        response = iam.attach_user_policy(UserName = target, PolicyArn = policy_arn)

    elif type == 'group':
        response = iam.attach_group_policy(GroupName = target, PolicyArn = policy_arn)
    print(response)

type = input("Would you like to attach the policy to a \'user\' or a \'group\'?")
if type == 'user':
    target = input("Enter the target user name: ")
elif type == 'group':
    target = input("Enter the target group name: ")
else:
    print('You must enter either \'user\' or \'group\'')
    exit()
policy_arn = input("Enter the arn of the policy to be attached: ")

attach_policy(policy_arn, target, type)