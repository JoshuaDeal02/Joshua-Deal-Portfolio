import boto3

def create_access_key(user):
    iam = boto3.client('iam')

    response = iam.create_access_key(UserName = user)
    print(response)

user = input('Input the name of the user to which the key will be added: ')
create_access_key(user)