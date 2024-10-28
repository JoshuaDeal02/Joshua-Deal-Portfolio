import boto3

db = boto3.resource('dynamodb')
table = db.Table('Employee')

response = table.scan()
data = response['Items']

print(response)