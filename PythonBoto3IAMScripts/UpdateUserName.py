import boto3

def update_user(old_username, new_username):
    iam = boto3.client('iam')

    response = iam.update_user(UserName=old_username, NewUserName=new_username)
    print(response)

old_username = input('Enter a Username to update')
new_username = input('Enter the new username')
update_user(old_username, new_username)