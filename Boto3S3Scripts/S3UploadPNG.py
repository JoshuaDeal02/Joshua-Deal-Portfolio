import boto3

s3 = boto3.client("s3")

with open("example.png", 'rb') as f:
    data = f.read()

response = s3.put_object(
    ACL="private",
    Bucket = "example-bucket9432",
    Body = data,
    Key = 'aws.png'
)
print(response)