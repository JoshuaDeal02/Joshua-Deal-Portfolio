import boto3

def add_user_to_group(user, group):
    iam = boto3.client('iam')

    response = iam.add_user_to_group(
        UserName = user,
        GroupName = group
    )

    print(response)
group = input('Input the name of the target group: ')
user = input('Input the name of the user to be added: ')
add_user_to_group(user, group)