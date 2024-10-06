import boto3

def delete_user(user):
    iam = boto3.client('iam')

    response = iam.delete_user(UserName = user)
    print(response)


user = input("Note that all policies, access keys, and groups must be removed from the user before deletion. \n Enter the user to be deleted: ")
delete_user(user)