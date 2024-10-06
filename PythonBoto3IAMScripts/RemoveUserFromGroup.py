import boto3

def remove_user_from_group(user, group):
    iam = boto3.resource('iam')
    group = iam.Group(group)

    response = group.remove_user(UserName = user)

    print(response)
group = input('Input the name of the target group: ')
user = input('Input the name of the user to be removed: ')
remove_user_from_group(user, group)