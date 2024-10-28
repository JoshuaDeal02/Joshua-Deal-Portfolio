import boto3

s3 = boto3.client('s3')

response = s3.delete_object(
    Bucket = 'first-bucket43',
    Key = 'copy.png'
)
print(response)