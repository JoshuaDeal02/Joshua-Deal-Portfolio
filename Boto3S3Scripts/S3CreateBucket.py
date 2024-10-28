import boto3

s3 = boto3.client("s3")
response = s3.create_bucket(
    Bucket = "example-bucket9432",
    ACL = "private",

    CreateBucketConfiguration = {
        'LocationConstraint':'us-east-2'
    }
)
print(response)