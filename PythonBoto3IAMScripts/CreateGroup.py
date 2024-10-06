import boto3

def create_group(name):
    iam = boto3.client('iam')

    response = iam.create_group(GroupName = name)
    print(response, '\nRun the AttachPolicy script to add policies to the group and the AddUserToGroup script to add users to the group')

name = input('Input the name of the new group: ')
create_group(name)