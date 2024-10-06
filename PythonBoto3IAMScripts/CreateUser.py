import boto3

def create_user(username):
    iam = boto3.client("iam")
    response = iam.create_user(UserName=username)
    print(response)
    
username = input("Input the new user's name: ")
create_user(username)